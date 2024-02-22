from django.db import models

# Create your models here.
class Location(models.Model):
	location = models.CharField(max_length=30)
