from django.urls import path
from . import views as app

urlpatterns = [
	path("home/", app.home, name="home"),
]