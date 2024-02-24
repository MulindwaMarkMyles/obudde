from django.shortcuts import render
import requests, datetime


# Create your views here.
def home(request):
	API_KEY  = open("./API_KEY", 'r').read()
	current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=imperial"
	forecast_url = "https://api.openweathermap.org/data/2.5/forecast?q={}&exclude=current,minutely,hourly,alerts&appid={}&units=imperial"

	if request.method == 'POST':
		city_one = request.POST.get("city_one")
		# city_two = request.POST.get("city_two", None)

		weather_data_one , daily_forecasts_one = fetch_weather_and_forecast(city_one, API_KEY, current_weather_url, forecast_url)

		# if city_two:
		# 	weather_data_one , daily_forecasts_one = fetch_weather_and_forecast(city_two, API_KEY, current_weather_url, forecast_url)
		# else:
		# 	weather_data_two, daily_forecasts_two = None, None

		context = {
				"weather_data_one": weather_data_one,
				"daily_forecasts_one": daily_forecasts_one,
				# "weather_data_two": weather_data_two,
				# "daily_forecasts_two": daily_forecasts_two
		}
		# print(context)
		return render(request, "weather/index.html")
	else:
		return render(request, "weather/index.html")

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
	response = requests.get(current_weather_url.format(city, api_key)).json()
	forecast_response = requests.get(forecast_url.format(city, api_key)).json()

	weather_data = {
		"city":city,
		"temperature": round(response['main']['temp'], 2),
		"description": response['weather'][0]['description'],
		"icon": response['weather'][0]["icon"]
	}

	daily_forecasts = []
	for daily_data in forecast_response['list'][:7]:
		info = ({
				"day":datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
				"min_temp": round(daily_data['main']['temp_min'], 2),
				"max_temp": round(daily_data['main']['temp_max'], 2),
				"description": daily_data['weather'][0]['description'],
				"icon": daily_data['weather'][0]["icon"]
			})
	if info not in daily_forecasts:
		daily_forecasts.append(info)
		
	for key in weather_data: print(key, ":", weather_data[key])
	print("\n\n")
	for forecast in daily_forecasts:
		for key in forecast: print(key, ":", forecast[key])
		print("\n")
	return weather_data, daily_forecasts

        