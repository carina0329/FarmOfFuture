# FarmOfFuture

## Overview
The FarmOfFuture app acts as a platform that efficiently collects satellite data from [Planet](https://www.planet.com/) and soil data from sensors installed throughout our research farm. This combination offers users an in-depth look at the farm, utilizing satellite images and sensor insights for valuable analysis.

## Tech Stack
The FarmOfFuture app is developed using Python and JavaScript. The backend is built with Python using the Django Framework, while the frontend is created with JavaScript using the Vue framework. The app incorporates essential dependencies like [Leaflet](https://leafletjs.com/) for overlaying satellite images on interactive maps, and [Chart.js](https://www.chartjs.org/docs/latest/) for visually presenting sensor data in an engaging manner.

## How to Run the Code
To run the code, open three terminal windows on your local device and follow these steps:
### Running the Data Listener
1. To initiate the data listener, open the first terminal window and execute the command `python init_app.py`. It's important to note that this step involves polling the satellite data archive from the past 30 days on [Planet](https://www.planet.com/). The duration of this process can vary, approximately taking around 10 minutes. The time taken is subject to the processing speed of [Planet](https://www.planet.com/) in handling image requests. Please make sure PL_API_KEY is set up properly.
[Please watch a demo video](https://drive.google.com/file/d/1fD93gQeetTbgsGiLpswLROMIrq-tW_T6/view?usp=sharing) that illustrates the workflow when app starts.
### Setting up Backend and Frontend
2. In a separate terminal window, initiate the backend server by executing the command `python manage.py runserver 8000`.
3. In another terminal window, navigate to the farm_of_future_frontend/ directory and run `npm run serve` to launch the frontend.

## Source of Data

### Satellite Imagery

To obtain satellite imagery data, follow these steps:

1. Get an API key from your Planet account.
2. Create a local .env file and include the line `PL_API_KEY=<your_API_key>` in it. Django uses this file to read the environment variable.
3. Alongside the data listener during app startup, when a user selects a date without available satellite data, we'll automatically request the image from Planet and display it. Please watch [a demo video](https://drive.google.com/file/d/1hD6eraIvUZCnXmTvUthuk6SPReJRLi_6/view?usp=sharing) that illustrates the this workflow.
### Sensor Data

To include sensor data, follow these steps:

1. The sensor data should be in CSV format.
2. The CSV file must have the following columns for proper parsing and insertion into the database: Date, Depth, Site, Plot, Year, Value.
3. Add the CSV file to the `sensor_data` folder in the main project directory.

### Future Work
Optimizing the app's startup time is a significant goal. Currently, the initialization process involves multiple stages: searching for targeted satellite images, placing orders for these images on Planet's platform, downloading the ordered images, and finally recording them in the app's database. Enhancing the efficiency of these steps, possibly through parallelization or improved data handling strategies, could notably reduce the app's initialization time and provide a smoother user experience.
