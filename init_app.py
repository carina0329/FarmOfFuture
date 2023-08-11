import os
from multiprocessing import Process
import time
from insert_image import *
from insert_data import *
from planet_api_requests import *


def check_for_new_sensor_file():
    print("checking sensor data......")
    dir_path = "sensor_data"
    last_seen = set()
    while True:
        files = set(name for name in os.listdir(dir_path) if not name.startswith('.'))
        new_files = files - last_seen
        for file_ in new_files:
            print(f"New sensor file detected: {file_}")
            insert_sensor_data(os.path.join(dir_path, file_))
        last_seen = files
        # time.sleep(2)

def check_for_new_satellite_folder():
    print("checking satellite data......")
    dir_path = "satellite_data/raster_files"
    last_seen = set()
    while True:
        # Get the list of non-hidden folders in the directory
        folders = set(name for name in os.listdir(dir_path) if not name.startswith('.'))
        # Find any new folders that were not seen in the last iteration
        new_folders = folders - last_seen
        # Print the names of the new folders
        for folder in new_folders:
            print(f"New folder detected: {folder}")
            insert_data_all(folder)
        # Update the set of last-seen folders
        last_seen = folders
        # Wait for some time before checking again
        # time.sleep(2)  # Check every 2 seconds

def check_for_satellite_data():
    while True:
        check_for_new_satellite_folder()

if __name__ == "__main__":
    # TODO: delete everything in the db
    # TODO: poll planet API to include to write data in the latest month
    delete_all_sensor_data()
    delete_all_satellite_data()
    # get the date today in YYYY-MM-DD
    # get the date 30 days back in YYYY-MM-DD
    date2 = datetime.now().strftime('%Y-%m-%d')
    date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    print(date)
    print(date2)
    item_ids = search(date, date2)
    print()
    if(len(item_ids) > 0):
        try:
            order_id = place_order(item_ids, "last_30days")
            download_order(order_id, "init_data")
        except:
            print("Error encountered during downloading order!")
            exit(1)
    download_order(order_id, "satellite_data")
    p1 = Process(target=check_for_new_sensor_file)
    p2 = Process(target=check_for_new_satellite_folder)
    p1.start()
    p2.start()
    p1.join()
    p2.join()