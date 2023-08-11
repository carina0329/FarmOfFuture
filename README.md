# FarmOfFuture

## Overview

The FarmOfFuture app is built using Python and JavaScript. The backend is developed with Python using the Django Framework, while the frontend utilizes JavaScript with the Vue framework.

## How to Run the Code

To run the code, follow these steps:

1. Open three terminal windows on your local device.
2. In the first terminal window, start the data listener by running `python check_new_data.py`.
3. In the second window, start the backend server by running `python manage.py runserver 8000`.
4. In the third window, navigate to the `farm_of_future_frontend/` directory and run `npm run serve` to start the frontend.

### Source of Data

#### Satellite Imagery

To obtain satellite imagery data, follow these steps:

1. Obtain a Planet API key from your Planet account portal.
2. Set up proper authentication by opening the terminal and setting the API key as an environment variable. For example, in macOS, use the command: `export PL_API_KEY='<Your API Key>'`.
3. After authentication, navigate to the `planet_api_requests.py` file. The Planet API requires searching for images within a specific date range, placing an order, and waiting for it to be processed. Once processed, the image can be downloaded to a desired folder. Here's an example of the workflow:

```python
items = search("2023-01-01", "2023-01-31")
order_id = place_order(items, "test_order")
download_order(order_id, 'satellite_data/raster_files/test')
```

#### Sensor Data

To include sensor data, follow these steps:

1. The sensor data should be in CSV format.
2. The CSV file must have the following columns for proper parsing and insertion into the database: Date, Depth, Site, Plot, Year, Value.
3. Add the CSV file to the `sensor_data` folder in the main project directory.

### Backend

The backend of the FarmOfFuture app is implemented using Python with the Django Framework. URLs and endpoints can be found in `mapApp/urls.py` and `mapApp/views.py`.

### Frontend

The frontend is developed using Vue.js. The Chart.js library is used to display the sensor data, while the Leaflet.js library is used to display the satellite data received from the backend.

### Work to be Done

Currently, developers need to manually load satellite data from Planet. However, work is underway to integrate this workflow into the frontend. When a user clicks on an unavailable date, the backend will trigger the workflow to fetch imagery from Planet. The estimated completion time for this integration is the end of June.
