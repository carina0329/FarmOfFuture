
# Import required modules
import csv
import sqlite3
import os

def delete_all_sensor_data():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    delete_records_sensor = "DELETE FROM mapApp_sensor"
    cursor.execute(delete_records_sensor)
    connection.commit()
    # # closing the database connection
    connection.close()

def insert_sensor_data(sensor_file_path):
    # Connecting to the database
    connection = sqlite3.connect('db.sqlite3')
    # Creating a cursor object to execute SQL queries on a database table
    cursor = connection.cursor()
    # Table Definition by model django
    # Opening the testSoilSmall.csv file
    file = open(sensor_file_path)
    # Reading the contents
    contents = csv.reader(file)
    # Skipping the first line
    next(contents)
    # For debugging. Delete data and reset the counter
    delete_records_sensor = "DELETE FROM mapApp_sensor"
    delete_sequence_sensor = "DELETE FROM SQLite_sequence WHERE name = 'mapApp_sensor'"
    # SQL query to insert data into the sensor table
    insert_records_sensor= "INSERT INTO mapApp_sensor (Date, Depth, Site, Plot, Year, Value) \
    VALUES(?, ?, ?, ?, ?, ?)"
    # perform the real insertion
    cursor.executemany(insert_records_sensor, contents)
    # cursor.execute(delete_records_sensor)
    # cursor.execute(delete_sequence_sensor)
    print("success")
    # # SQL query to retrieve all data from mapApp_sensor
    select_all_sensor = "SELECT * FROM mapApp_sensor"
    rows = cursor.execute(select_all_sensor).fetchall()
    print(len(rows))
    # # Output to the console screen
    for r in rows:
        print(r)
    # # Committing the changes
    connection.commit()
    # # closing the database connection
    connection.close()

def get_last_10_days():
    connection = sqlite3.connect('db.sqlite3')
    # Creating a cursor object to execute SQL queries on a database table
    cursor = connection.cursor()
    select_last10_sensor = "SELECT Date, Depth, Site, Plot FROM mapApp_sensor GROUP BY DATE ORDER BY DATE DESC LIMIT 10"
    rows = cursor.execute(select_last10_sensor).fetchall()
    lst = []
    for r in rows:
        lst.append(r)
    print(lst)
    connection.commit()
    # # closing the database connection
    connection.close()
    return lst

if __name__ == "__main__":
    # sensor_file_path = "sensor_data/Soilwc.csv"
    # insert_sensor_data(sensor_file_path)
    # get_last_10_days()
    delete_all_sensor_data()
    # pass