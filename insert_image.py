import sqlite3
import os
from sqlite3 import Error
from geotiff_viz import *
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
        result.append(r[0])
    connection.commit()
    # # closing the database connection
    connection.close()
    return result

# convert the image into blob
def convertPngToBlob(imagePath):
    with open(imagePath, 'rb') as file:
        binary = file.read()
    return binary

def insert_data_all(date):
    # find raster folder based on date
    rasterMainFolder = 'satellite_data/raster_files/'
    stSearch = date
    rasterFoldersOnDate = [rasterMainFolder + rasterFolder
                    for rasterFolder in os.listdir(rasterMainFolder) 
                    if stSearch in rasterFolder]
    print(rasterFoldersOnDate)
    # print(rasterFoldersOnDate)
    for rasterFolder in rasterFoldersOnDate:
        rasterFilesPath = rasterFolder + "/files"
        print(rasterFilesPath)
        for rasterFileName in os.listdir(rasterFilesPath):
            print(rasterFileName)
            f = os.path.join(rasterFilesPath, rasterFileName)
            # checking if it is a file
            if os.path.isfile(f):
                if f.endswith("tif") and "Analytic" in f:
                    print("------------")
                    print(f)
                    insert_image_data(f)

# insert in database the tif file with the specified path

def insert_image_data(rasterPath):
    try:
        connection = sqlite3.connect('db.sqlite3')
        print("Successful connection!")
        cursor = connection.cursor()
        rasterFileFolder = os.path.split(rasterPath)[0]
        rasterFileName = os.path.basename(rasterPath)
        rasterFileRoot = os.path.splitext(rasterFileName)[0]
        #construct imagePath from raster file path
        imageFileName = rasterFileRoot + '.png'
        imageFolder = "farm_of_future_frontend/public/satellite_data/image_files/"
        imageFilePath = os.path.join(imageFolder, imageFileName)
        # Write to the image file
        render_tiff(rasterPath, imageFilePath)
        imageFileBlob = convertPngToBlob(imageFilePath)
        # TODO: construct geojson path
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
        date = gj["properties"]["acquired"]
        date = date.split("T")[0]
        topleft = gj["geometry"]["coordinates"][0][0]
        topleftLat = topleft[1]
        topleftLng = topleft[0]
        topright = gj["geometry"]["coordinates"][0][3]
        toprightLat = topright[1]
        toprightLng = topright[0]
        bottomleft = gj["geometry"]["coordinates"][0][1]
        bottomleftLat = bottomleft[1]
        bottomleftLng = bottomleft[0]
        #now is the real insertion
        insertFileData = "INSERT INTO mapApp_satellite(RasterFileName, RasterFilePath, ImageFileName, ImageFilePath, ImageFileBlob, \
        Date, TopleftLat, TopleftLng, ToprightLat, ToprightLng, BottomleftLat, BottomleftLng)\
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)"
        cursor.execute(insertFileData, (rasterFileName, rasterPath, imageFileName, imageFilePath, imageFileBlob,
        date, topleftLat, topleftLng, toprightLat, toprightLng, bottomleftLat, bottomleftLng))
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


def read_image_data(date):
    try:
        connection = sqlite3.connect('db.sqlite3')
        print("Successful connection!")
        cursor = connection.cursor()
        imageData = "SELECT RasterFilePath,ImageFilePath,TopLeftLat,TopLeftLng,TopRightLat,TopRightLng,BottomLeftLat,BottomLeftLng FROM mapApp_satellite WHERE Date = ?"
        cursor.execute(imageData, (date, ))
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
            }
            resJsonObject.append(tmpJsonObject)
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.commit()
            connection.close()
            resJsonObjectStr = json.dumps(resJsonObject)
            print(resJsonObjectStr)
            return resJsonObjectStr
        else:
            error = "READ IMAGE DATA: There is an error somewhere!"
            print(error)

# for test purpose
def read_data_test(date):
    try:
        connection = sqlite3.connect('db.sqlite3')
        print("Successful connection!")
        cursor = connection.cursor()
        readFileData = "SELECT ImageFileBlob, ImageFilename FROM mapApp_satellite WHERE Date = ?"
        cursor.execute(readFileData, (date, ))
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
    # rasterPath_mar11 =
    # delete_data_all("mapApp_satellite")
    delete_data_all("mapApp_satellite")
    