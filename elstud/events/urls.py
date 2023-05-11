from django.urls import path

from .views import *
urlpatterns=[
    path('', index, name='events_index'),
    path('map', map_view, name='map'),
    path('add', add_event, name='add_event')
]