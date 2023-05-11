from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView

from .forms import *
from .models import *
from .utils import UserProfileMixin


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    context = {'form': form, 'tittle': 'Вход в учетную запись'}
    return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def home_view(request):
    return render(request, 'home.html', {'user': request.user, 'tittle': 'Главная страница'})

@permission_required('auth.add_user')
def create_new_user_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            return redirect('home')
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    return render(request, 'new_user.html', {'user_form' : user_form, 'user_profile_form': user_profile_form,
                                             'tittle' : 'Создание нового пользователя'})


@permission_required('auth.add_user')
def user_managment_view(request):
    return render(request, 'user_managment.html', {'tittle': 'Управление пользователями'})


@permission_required('auth.add_user')
def user_list_view(request):
    user_profiles_list = UserProfile.objects.all()
    group = request.GET.get('group', '')
    organization_name = request.GET.get('organization_name', '')
    is_student = request.GET.get('is_student', False)
    query = request.GET.get('q')

    if request.method =='GET':
        if group:
            user_profiles_list = user_profiles_list.filter(group=group)
        if organization_name:
            user_profiles_list = user_profiles_list.filter(organization_name=organization_name)
        if is_student:
            user_profiles_list = user_profiles_list.filter(is_student=True)
        if query:

            users = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))

            user_profiles_list = UserProfile.objects.filter(user__in=users).select_related('user')
        else:
            users = [profile.user for profile in user_profiles_list]


    context = {
        'tittle': 'Список пользователей',
        'user_profiles': user_profiles_list,
        'groups': UserProfile.objects.exclude(group='').values_list('group', flat=True).distinct(),
        'organizations': UserProfile.objects.exclude(organization_name='').values_list('organization_name', flat=True).distinct(),
        'users': users
    }
    return render(request, 'user_list.html', context)


@permission_required('auth.add_user')
def edit_user_profile(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    us = user_profile.user

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        user_form=UserEditForm(request.POST, instance=us)
        if user_profile_form.is_valid() and user_form.is_valid():
            user_profile_form.save()
            if user_profile_form.cleaned_data['is_user_manager']:
                user_manager_group = Group.objects.get(name='user_managers')
                user_manager_group.user_set.add(us)
            user_form.save()
            return redirect('user_list')
    else:
        user_profile_form = UserProfileForm(instance=user_profile)
        user_form = UserEditForm(instance=us)

    context = {
        'tittle': 'Редактирование пользователя ' + us.username,
        'user_profile': user_profile,
        'us': us,
        'user_form': user_form,
        'user_profile_form': user_profile_form
    }
    return render(request, 'edit_user_profile.html', context)


@permission_required('auth.add_user')
def change_password(request, slug):
    user = UserProfile.objects.get(slug=slug).user

    if request.method == 'POST':
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Обновляем сессионный ключ, чтобы пользователь оставался авторизованным
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль успешно изменен")
            return redirect('user_list')
    else:
        form = SetPasswordForm(user=user)
    context = {
        'form': form,
        'tittle': 'Смена пароля ' + user.username,
    }
    return render(request, 'change_password.html', context)