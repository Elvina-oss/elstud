from django.conf.urls.static import static
from django.urls import path

from .views import *
urlpatterns=[
    path('event_list/', event_list_map, name='event_list'),
    path('add_event/', add_event, name='add_event'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
