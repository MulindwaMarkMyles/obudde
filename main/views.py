from django.shortcuts import render
import requests, datetime


# Create your views here.
def home(request):
	API_KEY  = open("../API_KEY", 'r').read()
	current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
	forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

	if request.method == 'POST':
		city_one = request.POST.get("city_one")
		city_two = request.POST.get("city_two", None)

		weather_data_one , daily_forecasts_one = fetch_weather_and_forecast(city_one, API_KEY, current_weather_url, forecast_url)

		if city_two:
			weather_data_one , daily_forecasts_one = fetch_weather_and_forecast(city_two, API_KEY, current_weather_url, forecast_url)
		else:
			weather_data_two, daily_forecasts_two = None, None

		context = {
				"weather_data_one": weather_data_one,
				"daily_forecasts_one": daily_forecasts_one,
				"weather_data_two": weather_data_two,
				"daily_forecasts_two": daily_forecasts_two
		}
		
		return render(request, "weather/index.html")
	else:
		return render(request, "weather/index.html")

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
	response = requests.get(current_weather_url.format(city, api_key)).json()
	lat, lon = response['coord']['lat'], response['coord']['lon']
	forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

	weather_data = {
		"city":city,
		"temperature": round(response['main']['temp'] - 273.15, 2),
		"description": response['weather'][0]['description'],
		"icon": response['weather'][0]["icon"]
	}

	daily_forecasts = []
	for daily_data in forecast_response['daily'][:5]:
		daily_forecasts.append(({
				"day":datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
				"min_temp": round(daily_data['temp']['min'] - 273.15, 2),
				"min_temp": round(daily_data['temp']['max'] - 273.15, 2),
				"description": daily_data['weather'][0]['description'],
				"icon": daily_data['weather'][0]["icon"]
			}))

	return weather_data, daily_forecasts
