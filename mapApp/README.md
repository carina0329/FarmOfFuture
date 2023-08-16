
## Backend Endpoints

The FarmOfFuture app's backend exposes several endpoints to interact with and retrieve data. Below are the available endpoints along with their descriptions:

### `viewsensordata`

- **Method:** GET
- **Endpoint:** `/viewsensordata`

This endpoint allows you to retrieve sensor data. It handles the retrieval of sensor-related information and responds with the corresponding data.

### `viewsatellitedata`

- **Method:** GET
- **Endpoint:** `/viewsatellitedata/(date)`

This endpoint retrieves satellite data for a specified date that is cached locally. The date parameter in the URL allows you to fetch satellite data for the provided date.

### `insertsatellitedata` (DEPRECATED)

- **Method:** POST
- **Endpoint:** `/insertsatellitedata/(date)`

This endpoint enables you to insert satellite data for a specific date. It accepts POST requests with the desired date parameter in the URL and allows you to store satellite data.

### `getavailabledate`

- **Method:** GET
- **Endpoint:** `/getavailabledate/`

This endpoint provides available dates for which satellite data is accessible. It responds with a list of dates that have satellite images available.

### `getlast10`

- **Method:** GET
- **Endpoint:** `/getlast10/`

This endpoint retrieves the last ten sensor data entries. It allows you to quickly access the most recent sensor information.

### `getsatellitedata`

- **Method:** GET
- **Endpoint:** `/getsatellitedata/(date)`
This endpoint fetches satellite data for a specified date from Planet API and then insert it locally. Subsequent GET requests to access satellite images on the same date will be handled by `/viewsatellitedata/(date)`.

Please ensure you follow the appropriate HTTP methods and provide the required parameters as specified in each endpoint's description. These endpoints are crucial for interacting with and retrieving data from the FarmOfFuture app's backend.
