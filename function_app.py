import json
import requests
import azure.functions as func

app = func.FunctionApp()
@app.function_name(name="GetWeather")
@app.route(route="zipCode", methods=['GET', 'POST', 'OPTIONS'])
def main(req: func.HttpRequest) -> func.HttpResponse:
    apiKey = apiKey

    # Get the Zip code from the request body.
    reqBody = req.get_json()
    zipCode = reqBody.get('zipCode')

    # Checking to see if a Zip code is provided.
    if zipCode is None:
        return func.HttpResponse("Zip Code is required.", status_code=400)

    try:
        # Call the Weather API:
        callAPI = requests.get(f'http://api.openweathermap.org/geo/1.0/zip?zip={zipCode}&appid={apiKey}')

        # Check to see if the callAPI was successful
        if callAPI.status_code == 200:
            # Parse Data
            data = callAPI.json()

            # Extracting relevant information
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

            callAPIGetWeather = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={apiKey}')

            if callAPIGetWeather.status_code == 200:

                # Parse Data
                weatherData = callAPIGetWeather.json()

                # Extracting relevant information
                tempKelvin = weatherData.get('current', {}).get('temp', '')
                feelsLikeKelvin = weatherData.get('current', {}).get('feels_like', '')
                humidity = weatherData.get('current', {}).get('humidity', '')
                windSpeed = weatherData.get('current', {}).get('wind_speed', '')
                forecastSummary = weatherData.get('daily', [])[0].get('summary', '')

                tempFahrenheit = round((tempKelvin - 273.15) * 9/5 + 32)
                feelsLikeFahrenheit = round((feelsLikeKelvin - 273.15) * 9/5 + 32)


                tempFahrenheit = f'{tempFahrenheit}°F'
                feelsLikeFahrenheit = f'{feelsLikeFahrenheit}°F'
                humidity = f'{humidity}%'
                windSpeed = f'{windSpeed}mph'


                # Creating a dictionary to store the parsed data
                parsedWeatherData = {
                    'Location': name,
                    'Tempature': tempFahrenheit,
                    'Feels like': feelsLikeFahrenheit,
                    'Humidity': humidity,
                    'Wind Speed': windSpeed,
                    'Forecast Summary': forecastSummary
                }

                jsonDataWeather = json.dumps(parsedWeatherData)

                print(name, tempFahrenheit, feelsLikeFahrenheit, humidity, windSpeed, forecastSummary)

                # Creating the HTTP response
                response = func.HttpResponse(jsonDataWeather, mimetype="application/json")

                # Adding CORS headers
                if req.method == "OPTIONS":
                    response.headers["Access-Control-Allow-Origin"] = "*"
                    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
                    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept, Authorization, X-Request-With"
                
                response.headers["Access-Control-Allow-Origin"] = "*"  # Add this line outside the OPTIONS check

                return response

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)