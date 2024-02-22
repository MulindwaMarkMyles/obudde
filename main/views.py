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
