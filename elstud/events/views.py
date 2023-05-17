
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from events.forms import *
from events.models import *


def event_list(request):
    events = Event.objects.all()
    data = serializers.serialize('json', events)
    return JsonResponse(data, safe=False)


def event_list_map(request):
    api_key = settings.YANDEX_MAP_API
    context = {
        'api_key': api_key,
        'title': 'Карта событий',
    }
    return render(request, 'map.html', {'api_key': api_key})


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.latitude = request.POST.get('latitude')
            event.longitude = request.POST.get('longitude')
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    context = {
        'form': form,
        'title': 'Создание события',
        'api_key': settings.YANDEX_MAP_API,
    }
    return render(request, 'add_event.html', context)
