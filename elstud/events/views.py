from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, TemplateView, DetailView

from events.forms import *
from events.models import *
import json

api_key = settings.YANDEX_MAP_API


@login_required
def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.organizator = get_object_or_404(UserProfile, user=request.user)
            return redirect('home')
    form = EventForm()
    context = {
        'form': form,
        'tittle': 'Добавление события',
        'api_key': api_key,
    }
    return render(request, 'new_event.html', context)


class EventsListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    queryset = Event.objects.select_related('organizator__user').prefetch_related('organizator')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Список событий'
        return context


def events_map(request):
    template_name = 'event_map.html'
    events = Event.objects.select_related('organizator__user').prefetch_related('organizator')
    context = {
        'events': events,
        'tittle': 'Карта событий',
        'api_key': api_key,
    }
    return render(request, template_name, context)


class EventDetail(DetailView):
    template_name = 'event_detail.html'
    model = Event
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = context['event']
        event = self.object
        context['userProfile_org'] = event.organizator
        context['user_org'] = context['userProfile_org'].user

        return context


@login_required
def event_visitor(request):
    if request.method == 'POST':
        # Process the form data and create the EventVisitor object
        event_slug = request.POST.get('event_slug')
        assurance = request.POST.get('assurance')
        event = get_object_or_404(Event, slug=event_slug)
        EventVisitor.objects.create(user=request.user, event=event, assurance=assurance)
        return redirect(request.path)
    else:
        print('wtfff')
        return redirect('home')

def main(request):
    render(request, 'event_main')
