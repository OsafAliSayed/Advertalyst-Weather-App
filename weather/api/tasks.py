from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import City, Weather
from .key import KEY
import requests

@shared_task
def update_weather():
    # Get all cities
    cities = City.objects.all()

    for city in cities:
        # Make API call
        
        url = f'https://api.weatherapi.com/v1/current.json?key={KEY}&q={city.name}'
        response = requests.get(url).json()

        # Update weather data
        try:
            weather = Weather.objects.get(city=city)
            weather.temparature = response['current']['temp_c'],
            weather.humidity = response['current']['humidity'],
            weather.condition = response['current']['condition']['text'],
            weather.icon_url = response['current']['condition']['icon']
            weather.save()
            
        except Weather.DoesNotExist:
            weather = Weather(
                city=city,
                temparature = response['current']['temp_c'],
                humidity = response['current']['humidity'],
                condition = response['current']['condition']['text'],
                icon_url = response['current']['condition']['icon'],
            )
            weather.save()