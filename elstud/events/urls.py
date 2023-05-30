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
    path('my_events', MyEventsList.as_view(), name='my_events'),
    path('visitors/<slug:slug>/', EventVisitors.as_view(), name='event_visitors'),
    path('edit/<slug:slug>/', edit_event, name='edit_event'),
    path('event_managment/', EventManagmentList.as_view(), name='event_managment'),
    path('approve-event/', approve_event, name='approve_event'),
    path('delete-event/', delete_event, name='delete_event'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
