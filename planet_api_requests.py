import os
import json
import requests
import geojsonio
import time
import shutil
from datetime import datetime, timedelta

# Authenticate
API_KEY = os.environ.get('PL_API_KEY', '')
# Set URL
DATA_URL = "https://api.planet.com/data/v1/quick-search"
ORDER_URL = "https://api.planet.com/compute/ops/orders/v2"
COORDINATES_FARM = [[-88.21403682638878, 40.069036142012],
[-88.20924301795053, 40.06912901675976],[-88.20926324499034, 40.065460367934776],
[-88.21395591822947,40.06539844811567],[-88.21403682638878,40.069036142012]]
ITEM_TYPES = ["PSScene"]
ASSET_FILTER = { "type": "AssetFilter", "config": ["ortho_visual"]}
GEOMETRY_FILTER = {"type": "GeometryFilter", "field_name": "geometry","config": {"type": "Polygon", "coordinates": [COORDINATES_FARM]}}
def search(date, date2=None):
    # "2023-06-10T22:10:18.680Z"
    date_gt_obj = datetime.strptime(date, "%Y-%m-%d")
    date_lt_obj = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
    formatted_date_gt = date_gt_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    formatted_date_lt = date_lt_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    if date2:
        date_lt_obj = datetime.strptime(date2, "%Y-%m-%d") + timedelta(days=1)
        formatted_date_lt = date_lt_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    DATE_FILTER = {"type": "DateRangeFilter", "field_name": "acquired", "config": {"gt": formatted_date_gt,"lt": formatted_date_lt}}
    search_res_item_list = []
    session = requests.Session()
    session.auth = (API_KEY, "")
    search_filters = {
        "type": "AndFilter",
        "config": [
            ASSET_FILTER,
            DATE_FILTER,
            GEOMETRY_FILTER
        ]
    }
    request = {
        "item_types" : ITEM_TYPES,
        "filter" : search_filters
    }
    # Send the POST request to the API stats endpoint
    res = session.post(DATA_URL, json=request)
    for feature in res.json()["features"]:
        search_res_item_list.append(feature['id'])
    return search_res_item_list

def place_order(item_ids, order_name):
    print("Preparing to place an order with {} items".format(len(item_ids)))
    session = requests.Session()
    session.auth = (API_KEY, "")
    request = {
        "name": order_name,
        "source_type": "scenes",
        "products": [
            {
                "item_ids": item_ids,
                "item_type": "PSScene",
                "product_bundle": "visual"
            }
        ],
        "tools": [
            {
                "clip": {
                    "aoi": {
                        "type": "Polygon",
                        "coordinates": [
                            COORDINATES_FARM
                        ]
                    }
                }
            }
        ]
    }

    res = session.post(ORDER_URL, json=request)
    return res.json()["id"]

def download_order(order_id, download_dir):
    print("Preparing to download order with id {}".format(order_id))
    download_directory_path = os.path.join("satellite_data/raster_files", download_dir)
    if os.path.exists(download_directory_path):
        shutil.rmtree(download_directory_path)
    os.makedirs(download_directory_path)
    session = requests.Session()
    session.auth = (API_KEY, "")
    check_url = ORDER_URL + "/" + order_id
    while(session.get(check_url).json()["state"] != "success"):
        time.sleep(10)
        cur_state = session.get(check_url).json()["state"]
        if(cur_state == "failed" or cur_state == "cancelled"):
            raise Exception("Order Failed! Please retry search and order!")
            return
    res = session.get(check_url)
    result_files = res.json()["_links"]["results"]
    print(len(result_files))
    for result_file in result_files:
        result_file_name = result_file["name"]
        result_file_location = result_file["location"]
        result_file_name_local = os.path.basename(result_file_name)
        result_file_path_local = os.path.join(download_directory_path, result_file_name_local)
        res_download = session.get(result_file_location)
        with open(result_file_path_local, "wb") as file_:
            for chunk in res_download.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    file_.write(chunk)
                    file_.flush()

