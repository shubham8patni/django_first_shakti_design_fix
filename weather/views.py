import requests
import os
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    API_KEY = os.environ.get("wapi_key")
    city = "London"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    url = f"{BASE_URL}?appid={API_KEY}&q={city}"

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()
    
    form = CityForm()
    cities = City.objects.all()

    weather_data =[]
    for city in cities:
        r = requests.get(url).json()
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request,'weather/weather.html', context)