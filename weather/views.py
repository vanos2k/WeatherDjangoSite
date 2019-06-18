from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    context = {}
    appid ='18975ee113b791199c12ec3dd546776e'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID='+appid

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            r = requests.get(url.format(form.cleaned_data['name'])).json()
            if r['cod'] != 200:
                context.update({'title': r['message']})
            elif not City.objects.filter(name=form.cleaned_data['name']).exists():
                form.save()  # сохранение в бд
            else:
                context.update({'title': 'This city already in table, look better'})

    form = CityForm()
    cities = City.objects.all()
    all_cities = []

    for city in cities:
        try:
            r = requests.get(url.format(city.name)).json()
            city_info = {
                'city': city.name,
                'temp': r['main']['temp'],
                'icon': r['weather'][0]['icon']
            }
        except:
            context.update({'title':'Error, incorrect city'})
            continue

        all_cities.append((city_info))

    context.update({'all_info': all_cities,
                    'form': form,
                    })

    return render(request, 'weather/index.html', context)
