from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView


from events.forms import EventForm

import requests


def index(request):
    context = {
        'tittle': 'События',
    }
    return render(request, 'map.html', context=context)


class MarkersMapView(TemplateView):
    """Markers map view."""
    template_name = "map.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Карта'
        return context

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


from django.shortcuts import render
from django.conf import settings
from .models import Event
import json

def map_view(request):
    events = Event.objects.all()
    markers = []
    for event in events:
        markers.append({
            'name': event.tittle,
            'lat': event.latitude,
            'lng': event.longitude,
        })

    center_lat = 55.796127
    center_lng = 49.106405

    return render(request, 'map.html', {
        'center_lat': center_lat,
        'center_lng': center_lng,
        'markers': json.dumps(markers),
        'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN,
    })
