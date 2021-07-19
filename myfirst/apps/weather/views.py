import datetime
import json

from django.shortcuts import render
import bs4
import requests
from django.utils import timezone
from background_task import background
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Min, Max, Avg

from .models import City


def index(request):
    city_list = City.objects.order_by('-city_name')
    return render(request, 'weather/list.html', {'city_list': city_list})


def detail(request, city_id):
        c = City.objects.get(id=city_id)
        weather_list = c.temperature_set.order_by('-date')
        return render(request, 'weather/detail.html', {'city': c, 'weather_list': weather_list})


def weather_by_city(city):
    city = city.lower()

    page = requests.get(f'https://sinoptik.com.ru/погода-{city}')

    if page.status_code == 404:
        raise ConnectionError('there is no city with this name')

    html = bs4.BeautifulSoup(page.text, "html.parser")

    res = html.select('.weather__article_main_temp')[0].getText()
    res = res.replace("\n", "")
    res = res.replace("°C", "")
    return res


@background(schedule=60)
def update_all_cities():
    cities = City.objects.order_by('-city_name')
    for city in cities:
        temp = weather_by_city(city.city_name)
        city.temperature_set.create(date=timezone.now(), temperature=temp)


def get_city(request):
    id = request.POST['city_id']
    c = City.objects.get(id=id)
    return c


def go_query(request, method):
    c = get_city(request)

    if method == 'min':
        temperature = c.temperature_set.aggregate(Min('temperature'))
    elif method == 'max':
        temperature = c.temperature_set.aggregate(Max('temperature'))
    elif method == 'avg':
        temperature = c.temperature_set.aggregate(Avg('temperature'))

    return c, temperature


@csrf_exempt
def now(request):
    if request.method == 'POST':
        c = get_city(request)
        temperature = weather_by_city(c.city_name)
        return JsonResponse({c.city_name: str(temperature)})


@csrf_exempt
def min(request):
    if request.method == 'POST':
        c, temperature = go_query(request, 'min')
        return JsonResponse({c.city_name: str(temperature['temperature__min'])})


@csrf_exempt
def max(request):
    if request.method == 'POST':
        c, temperature = go_query(request, 'max')
        return JsonResponse({c.city_name: str(temperature['temperature__max'])})


@csrf_exempt
def avg(request):
    if request.method == 'POST':
        c, temperature = go_query(request, 'avg')
        return JsonResponse({c.city_name: str(temperature['temperature__avg'])})


@csrf_exempt
def interval(request):
    if request.method == 'POST':
        date_from = request.POST['from']
        date_from = json.loads(date_from)
        date_from = datetime.datetime(date_from['year'], date_from['month'], date_from['day'])

        date_to = request.POST['to']
        date_to = json.loads(date_to)
        date_to = datetime.datetime(date_to['year'], date_to['month'], date_to['day'])

        c = get_city(request)
        temperature = c.temperature_set.exclude(date__gt=date_to)
        temperature = temperature.exclude(date__lt=date_from)

        res = [{str(elem.city_name): str(elem.temperature)} for elem in temperature]
        return JsonResponse(res, safe=False)
