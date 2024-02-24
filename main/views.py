from django.shortcuts import render
import requests, datetime


# Create your views here.
def fahrenheit_to_celsius(fahrenheit):
        celsius = (fahrenheit - 32) * 5/9
        return celsius

def home(request):
	API_KEY  = open("./API_KEY", 'r').read()
	current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=imperial"
	forecast_url = "https://api.openweathermap.org/data/2.5/forecast?q={}&exclude=current,minutely,hourly,alerts&appid={}&units=imperial"

	if request.method == 'POST':
		city_one = request.POST.get("city_one")

		weather_data , daily_forecasts = fetch_weather_and_forecast(city_one, API_KEY, current_weather_url, forecast_url)
		context = {
				"weather_data": weather_data,
				"daily_forecasts": daily_forecasts,
		}
		return render(request, "weather/index.html", context)
	else:
		return render(request, "weather/index.html")

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
	response = requests.get(current_weather_url.format(city, api_key)).json()
	forecast_response = requests.get(forecast_url.format(city, api_key)).json()

	weather_data = {
		"city":city,
		"temperature": round(fahrenheit_to_celsius(response['main']['temp']), 2),
		"description": response['weather'][0]['description'],
		"icon": response['weather'][0]["icon"]
	}

	daily_forecasts = []
	for daily_data in forecast_response['list'][:7]:
		info = {
				"day":datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
				"min_temp": round(fahrenheit_to_celsius(daily_data['main']['temp_min']),2),
				"max_temp": round(fahrenheit_to_celsius(daily_data['main']['temp_max']), 2),
				"description": daily_data['weather'][0]['description'],
				"icon": daily_data['weather'][0]["icon"]
			}
	if info not in daily_forecasts:
		daily_forecasts.append(info)
		
	return weather_data, daily_forecasts

        