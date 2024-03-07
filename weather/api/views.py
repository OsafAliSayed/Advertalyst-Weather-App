from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from django.views import View
from django.conf import settings

import jwt
import json
import requests
from datetime import datetime, timedelta

from .models import City, Weather
from .key import KEY


def weather(request):
    # get cities from request
    cities = []
    
    # check if cities where passed in
    if request.GET.getlist('cities'):
        cities = request.GET.getlist('cities')[0].split(',')
    else:
        return JsonResponse({'error': 'no cities provided'}, status=400)
    
    # create a dict to hold the response
    res = {}
    objs = []
    # query weatherapi.com for city weathers http://api.weatherapi.com/v1
    for city in cities:
        url = f'https://api.weatherapi.com/v1/current.json?key={KEY}&q={city}'
        response = requests.get(url)
        if response.status_code == 500:
            # check if weather information has been stored locally
            try:
                # create new obj here
                weather = Weather.objects.get(city=city)
                obj = {
                    "name": weather.city.name,
                    "country": weather.city.country,
                    "temperature": weather.temperature,
                    "humidity": weather.humidity,
                    "condition": weather.condition,
                    "icon_url": weather.icon_url
                }
                # append to objs list
                objs.append(obj)
                continue
            # otherwise throw error
            except Weather.DoesNotExist:
                return JsonResponse({'error': 'Internal Server Error'}, status=500)
            
        #  throw error if city name is invalid or not given
        if response.status_code != 200:
            return JsonResponse({'error': 'Bad Request(Invalid City names)'}, status=400)
        
        # after error handling convert to json and create a temporary object
        response = response.json()
        obj = {
            "name": response['location']['name'],
            "country": response['location']['country'],
            "temperature": response['current']['temp_c'],
            "humidity": response['current']['humidity'],
            "condition": response['current']['condition']['text'],
            "icon_url": response['current']['condition']['icon'],
        }
        objs.append(obj)
    res['example'] = {
        "cities" : objs
    }
    
    return JsonResponse(res, safe=False)
        
@csrf_exempt        
def city(request, id):
    # handling GET Request
    if request.method == 'GET':
        try:
            city = City.objects.get(id=id)
            return JsonResponse({"example" : {
                "id": city.id,
                "name": city.name, 
                "country": city.country
            }}, status=200)
        except City.DoesNotExist:
            return JsonResponse({ "example": {
                "error": "City not found"
            }}, status=404)
        
    # Handling PUT request
    if request.method == 'PUT':
        try:
            # get relevant city
            city = City.objects.get(id=id)
            body = json.loads(request.body.decode('utf-8'))
            
            if 'example' in body:
                # update name if exist
                if 'name' in body['example']:
                    city.name = body['example']['name']
                    city.save()
                else:
                    return JsonResponse({ "example": {
                        "error": "name is required"
                    }}, status=400)
                
                # update country if exist
                if 'country' in body['example']:
                    city.country = body['example']['country']
                    city.save()
                    
                return JsonResponse({ "example": {
                    "id": city.id,
                    "name": city.name, 
                    "country": city.country
                }}, status=200)
                
        except City.DoesNotExist:
            return JsonResponse({ "example": {
                "error": "City not found"
            }}, status=404)
        
    # Handling DELETE request
    if request.method == 'DELETE':
        try:
            # Get relevant city and delete it
            city = City.objects.get(id=id)
            city.delete()
            return JsonResponse({ "example": {
                "message": "City deleted"
            }}, status=200)
            
        except City.DoesNotExist:
            return JsonResponse({ "example": {
                "error": "City not found"
            }}, status=404)
            
@csrf_exempt        
def auth(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf-8'))
        username = response['username']
        password = response['password'] 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=60)
            }
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            print(jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256']))
            return JsonResponse({'token': jwt_token})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)