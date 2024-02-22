from django.urls import path
from . import views as app

urlpatterns = [
	path("", app.home, name="home"),
]