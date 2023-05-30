from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView

from events.forms import *
from events.models import *
import json

api_key = settings.YANDEX_MAP_API


@login_required
def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizator = get_object_or_404(UserProfile, user=request.user)
            event.save()
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
    current_date = datetime.now()
    queryset = Event.objects.filter(time_end__gt=current_date).select_related('organizator__user').prefetch_related('organizator')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Список событий'
        return context



@login_required
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

    def get_queryset(self):
        return Event.objects.filter(slug=self.kwargs['slug'])

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

@login_required
def main(request):
    context = {
        'tittle': 'Мероприятия',
    }
    return render(request, 'event_main.html', context)


class MyEventsList(ListView):
    model = Event
    template_name = 'my_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return super().get_queryset().filter(organizator__user=self.request.user).select_related('organizator__user').prefetch_related('organizator')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Мои мероприятия'
        return context


class EventVisitors(ListView):
    model = EventVisitor
    template_name = 'event_visitors.html'
    context_object_name = 'visitors'

    def get_queryset(self):
        event_slug = self.kwargs['slug']
        event = get_object_or_404(Event, slug=event_slug)
        visitors = EventVisitor.objects.filter(event=event).select_related('user__userprofile')

        assurance_param = self.request.GET.get('assurance')
        if assurance_param == 'False':
            visitors = visitors.filter(assurance=False)
        elif assurance_param == 'True':
            visitors = visitors.filter(assurance=True)
        return visitors

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        event_slug = self.kwargs['slug']
        event = get_object_or_404(Event, slug=event_slug)

        context['event'] = event
        context['total_count'] = EventVisitor.objects.filter(event=event).count()
        context['assurance_false_count'] = EventVisitor.objects.filter(event=event, assurance=False).count()
        context['assurance_true_count'] = EventVisitor.objects.filter(event=event, assurance=True).count()
        return context


@login_required
def edit_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            event.save()
            return redirect('my_events')
    form = EventForm(instance=event)
    context = {
        'form': form,
        'tittle': 'Редактировать событие ' + event.title,
        'api_key': api_key,
    }
    return render(request, 'edit_event.html', context)


def event_managment(request):
    context = {
        'tittle': 'Управление событиями'
    }
    return render(request, 'event_managment.html', context)

class EventManagmentList(ListView):
    model = Event
    template_name = 'event_managment.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = Event.objects.filter(approved=False).select_related('organizator__user').prefetch_related(
            'organizator')
        print('w')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Управление событиями'

        return context


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@permission_required('shop.change_event')
@csrf_exempt
def approve_event(request):
    if request.method == 'POST' and is_ajax(request):
        event_id = request.POST.get('event_id')
        event = Event.objects.get(id=event_id)
        event.approved = True
        event.save()
        return JsonResponse({'message': 'Event approved successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'})

@csrf_exempt
def delete_event(request):
    if request.method == 'POST' and is_ajax(request):
        event_id = request.POST.get('event_id')
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'message': 'Event deleted successfully'})
        except:
            return JsonResponse({'error': 'Event not found.'}, status=404)

    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)