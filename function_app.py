import azure.functions as func
import logging
import requests
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="getWeather")
def getWeather(req: func.HttpRequest) -> func.HttpResponse:
    apiKey = "e7a3b43fa8694572384ca1be977b2c42"

    # Get the Zip code from the query parameters.
    reqBody = req.get_json()
    zipCode = req.params.get('zip')

    # Legacy zipCode input
    # zipCode = input("Enter a zip code: ")

    # Checking to see if a Zip code is provided.
    if not zipCode:
        return func.HttpResponse("Zip Code is required.", status_code=400) 


    # Call the Weather API:
    callAPI = requests.get(f'http://api.openweathermap.org/geo/1.0/zip?zip={zipCode}&appid={apiKey}')

    # Check to see if the callAPI was successful
    if callAPI.status_code == 200:
        # Parse Data
        data = callAPI.json()

        # Extracting relevan information
        zipCodeResult = data.get('zip', '')
        name = data.get('name', '')
        lat = data.get('lat', 0.0)
        lon = data.get('lon', 0.0)
        country = data.get('country', '')

        # Creating a dictionary to store the parsed data
        parsedData = {
            'zip': zipCodeResult,
            'name': name,
            'lat': lat,
            'lon': lon,
            'country': country
        }
    
        jsonData = json.dumps(parsedData)

            # Creating the HTTP response
    response = func.HttpResponse(jsonData, mimetype="application/json")

# Adding CORS headers
    if req.method == "OPTIONS":
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept, Authorization, X-Request-With"

    return response

    # Handling non-success status code
    return func.HttpResponse(f"API request failed with status code {callAPI.status_code}", status_code=callAPI.status_code)