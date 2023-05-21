from django.conf.urls.static import static
from django.urls import path

from .views import *
urlpatterns=[
    path('new_event/', new_event, name='new_event'),
    path('event_list/', EventsListView.as_view(), name='event_list'),
    path('event_map/', events_map, name='event_map'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
