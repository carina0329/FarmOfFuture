import random
import datetime
import csv

def generate_records(output_file):
    # Define lists of possible values for each column
    depths = [10, 20, 30, 50]
    sites = ['IN_Randolph', 'MN_Redwood1', 'OH_Auglaize2', 'SD_Clay', 'energyFarm']
    plots = ['SW', 'MaizeControl', 'BE', 'WS']
    site = "energyFarm"
    plot = "WS"
    depth = random.choice(depths)
    # Generate 100 records
    records = []
    current_date = datetime.date(2021, 9, 1)
    for i in range(100):
        # Increment the date by one day for each record
        current_date += datetime.timedelta(days=1)
        # Select random values for the other columns
        value = round(random.uniform(0, 1), 2)
        # Add the record to the list
        record = [current_date.strftime('%Y-%m-%d'), depth, site, plot, current_date.year, value]
        records.append(record)

    # Write the records to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Depth', 'Site', 'Plot', 'Year', 'Value'])
        for record in records:
            writer.writerow(record)

if __name__ == "__main__":
    generate_records('sensor_data/soil_data6.csv')