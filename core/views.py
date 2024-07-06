# core/views.py
from datetime import datetime

from django.http import HttpResponse, JsonResponse
import requests

API_KEY = 'f78d1a8ba4eb7ced58dc0669866bee59'

def index(request):
    return HttpResponse('Hello world.')

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = request.META.get('REMOTE_ADDR')

    # Fetch location information
    location_response = requests.get(f'https://ipinfo.io/{client_ip}/json')
    location_data = location_response.json()
    city = location_data.get('city', 'Unknown location')

    # Fetch weather information
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}')
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp']

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    return JsonResponse(response)