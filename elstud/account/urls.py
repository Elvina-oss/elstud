# from django.urls import path
#
# from .views import *
#
# urlpatterns=[
#     path('', LoginUser.as_view(), name='login')
# ]

from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_new_user/', create_new_user_view, name='create_new_user'),
    path('user_managment/', user_managment_view, name='user_managment'),
    path('user_list/', user_list_view, name='user_list'),
    path('<slug:slug>/edit', edit_user_profile, name='edit_user'),
    path('<slug:slug>/password', change_password, name='change_password'),

]