import sqlite3
import os
from sqlite3 import Error
from geotiff_viz_4band import *
from datetime import datetime, time, timedelta
import geojson
import json

def get_satellite_available_dates():
    result = []
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    get_dates_sensor = "SELECT DISTINCT Date FROM mapApp_satellite"
    cursor.execute(get_dates_sensor)
    record = cursor.fetchall()
    for r in record:
        date = r[0].split('T')[0]
        if date not in result:
            result.append(date)
    connection.commit()
    # # closing the database connection
    connection.close()
    return result

# convert the image into blob
def convertPngToBlob(imagePath):
    with open(imagePath, 'rb') as file:
        binary = file.read()
    return binary
def insert_data_on_date(date):
    rasterMainFolder = 'satellite_data/raster_files/'

def insert_data_all(folder_name):
    # find raster folder based on date
    raster_main_folder = 'satellite_data/raster_files/'
    raster_folder_path = os.path.join(raster_main_folder, folder_name)
    for root, dirs, files in os.walk(raster_folder_path):
        for raster_file in files:
            if raster_file.endswith(".tif"):
                filepath = os.path.join(root, raster_file)
                print("Tif file found: \t", filepath)
                insert_image_data(filepath)

def insert_image_data(rasterFilePath):
    try:
        connection = sqlite3.connect('db.sqlite3')
        print("Successful connection!")
        cursor = connection.cursor()
        rasterFileFolder = os.path.split(rasterFilePath)[0]
        # print("rasterFileFolder: \t", rasterFileFolder)
        rasterFileName = os.path.basename(rasterFilePath)
        # print("rasterFileName: \t", rasterFileName)
        rasterFileRoot = os.path.splitext(rasterFileName)[0]
        # print("rasterFileRoot: \t", rasterFileRoot)
        #construct imagePath from raster file path
        imageFileName = rasterFileRoot + '.png'
        imageFolder = "farm_of_future_frontend/public/satellite_data/image_files/"
        imageFilePath = os.path.join(imageFolder, imageFileName)
        # print("imageFilePath: \t", imageFilePath)
        # Write to the image file
        render_tiff(rasterFilePath, imageFilePath)
        imageFileBlob = convertPngToBlob(imageFilePath)
        # # TODO: construct geojson path
        rasterFileList = rasterFileName.split("_")
        getjson_file = rasterFileList[0] + "_" + rasterFileList[1] + "_" + rasterFileList[2] + "_" + rasterFileList[3] + "_" + "metadata.json"
        getjson_path = os.path.join(rasterFileFolder, getjson_file)
        if os.path.exists(getjson_path):
            print("it exists")
            print(getjson_path)
        # TODO: ingest geojson
        with open(getjson_path) as f:
            gj = geojson.load(f)
        # TODO: make sure it is formatted correctly
        datetime = gj["properties"]["acquired"]
        topleft = gj["geometry"]["coordinates"][0][0]
        topleftLat = topleft[1]
        topleftLng = topleft[0]
        topright = gj["geometry"]["coordinates"][0][3]
        toprightLat = topright[1]
        toprightLng = topright[0]
        bottomleft = gj["geometry"]["coordinates"][0][1]
        bottomleftLat = bottomleft[1]
        bottomleftLng = bottomleft[0]
        print(datetime)
        print(topleft)
        print(topright)
        print(bottomleft)
        # print()
        # #now is the real insertion
        insertFileData = "INSERT INTO mapApp_satellite(RasterFileName, RasterFilePath, ImageFileName, ImageFilePath, ImageFileBlob, \
        Date, TopleftLat, TopleftLng, ToprightLat, ToprightLng, BottomleftLat, BottomleftLng)\
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(insertFileData, (rasterFileName, rasterFilePath, imageFileName, imageFilePath, imageFileBlob,
        datetime, topleftLat, topleftLng, toprightLat, toprightLng, bottomleftLat, bottomleftLng))
        selectFileData = "SELECT * FROM mapApp_satellite"
        cursor.execute(selectFileData)
        record = cursor.fetchall()
        print(len(record))
        connection.commit()
        print("Successful insertion operation!")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()
        else:
            error = "INSERT DATA: There is an error somewhere!"
            print(error)

def find_closest_to_noon(json_data):
    noon = time(12, 0, 0) # Set noon time as a datetime.time object
    closest_time = None
    closest_diff = timedelta.max
    for item in json_data:
        date_string = item["Date"]
        date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        # formatted_date = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        time_obj = date_obj.time() # Extract the time part of the datetime object
        # Calculate the time difference between the current time and noon
        diff = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second, microseconds=time_obj.microsecond) - timedelta(hours=noon.hour, minutes=noon.minute, seconds=noon.second)
        # If the current time difference is smaller than the current closest time difference, update closest_time and closest_diff
        if diff < closest_diff:
            closest_time = item
            closest_diff = diff
    return closest_time

def read_image_data(date):
    date_pattern = date + "%"
    try:
        connection = sqlite3.connect('db.sqlite3')
        print("Successful connection!")
        cursor = connection.cursor()
        imageData = "SELECT RasterFilePath,ImageFilePath,TopLeftLat,TopLeftLng,TopRightLat,TopRightLng,BottomLeftLat,BottomLeftLng,Date FROM mapApp_satellite WHERE Date LIKE ?"
        cursor.execute(imageData, (date_pattern, ))
        record = cursor.fetchall()
        resJsonObject = []
        print(len(record))
        for recordList in record:
            tmpJsonObject = {
                "RasterFilePath": recordList[0],
                "ImageFilePath": recordList[1],
                "TopLeftLat": recordList[2],
                "TopLeftLng": recordList[3],
                "TopRightLat": recordList[4],
                "TopRightLng": recordList[5],
                "BottomLeftLat": recordList[6],
                "BottomLeftLng": recordList[7],
                "Date":recordList[8]
            }
            resJsonObject.append(tmpJsonObject)
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.commit()
            connection.close()
            temp = find_closest_to_noon(resJsonObject)
            # print(temp)
            resJsonObjectStr = json.dumps(temp)
            # print(resJsonObjectStr)
            return resJsonObjectStr
        else:
            error = "READ IMAGE DATA: There is an error somewhere!"
            print(error)

# for test purpose
def read_data_test(date):
    date_pattern = date + "%"
    try:
        connection = sqlite3.connect('db.sqlite3')
        print("Successful connection!")
        cursor = connection.cursor()
        readFileData = "SELECT ImageFileBlob, ImageFilename FROM mapApp_satellite WHERE Date = ?"
        cursor.execute(readFileData, (date_pattern, ))
        record = cursor.fetchall()
        imgFilenameTempList = []
        for record_list in record:
            imgBlobTemp = record_list[0]
            print(len(imgBlobTemp))
            imgFilenameTemp = "test/" + record_list[1].split('.')[0] + '_tmp' + '.png'
            print(imgFilenameTemp)
            imgFilenameTempList.append(imgFilenameTemp)
            # write
            write_blob_data(imgBlobTemp, imgFilenameTemp)
        # print(record)
        # write_blob_data(record, localTempFile)
        connection.commit()
        print("Successful operation!")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()
            return imgFilenameTempList
        else:
            error = "READ DATA: There is an error somewhere!"

def write_blob_data(imageFileBlob, localTempFile):
    with open(localTempFile, 'wb') as file:
        file.write(imageFileBlob)
    print("Success! Data has been written to the local temp file: ", localTempFile)

def delete_data_all(tableName):
    connection = sqlite3.connect('db.sqlite3')
    print("Successful connection!")
    cursor = connection.cursor()
    delete_records_satellite = f"""
    DELETE FROM {tableName}
    """
    cursor.execute(delete_records_satellite)
    connection.commit()
    selectFileData = f"""
    SELECT *
    FROM {tableName}
    """
    cursor.execute(selectFileData)
    record = cursor.fetchall()
    print(len(record))
    connection.commit()
    connection.close()
    print("Successful deletion operation!")

if __name__ == "__main__":
    # pass
    # insert_image_data("2023_03_30_psscene_visual")
    # insert_data_all("2023_03_20_psscene_visual")
    # read_image_data("2023-03-20")
    # rasterPath_mar11 =
    # delete_data_all("mapApp_satellite")
    # insert_image_data("satellite_data/test/20230301_155145_86_24cc_3B_Visual_clip.tif")
    delete_data_all("mapApp_satellite")
    