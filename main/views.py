from django.shortcuts import render
import requests, datetime


# Create your views here.
def home(request):
	API_KEY  = open("../API_KEY", 'r').read()
	current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
	forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"