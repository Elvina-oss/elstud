from django.conf.urls.static import static
from django.urls import path

from .views import *
urlpatterns=[
    path('', main, name='event_main'),
    path('new_event/', new_event, name='new_event'),
    path('event_list/', EventsListView.as_view(), name='event_list'),
    path('event_map/', events_map, name='event_map'),
    path('event_detail/<slug:slug>', EventDetail.as_view(), name='event_detail'),
    path('event_visitor/', event_visitor, name='event_visitor'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
