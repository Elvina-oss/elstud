
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError

from account.models import UserProfile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))


class UserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'autofocus': True}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']



class UserProfileForm(forms.ModelForm):
    is_student = forms.BooleanField(label='Студент', widget=forms.CheckboxInput(), required=False)
    group = forms.CharField(label='Номер группы', widget=forms.TextInput(), required=False)
    organization_name = forms.CharField(label='Название организации', widget=forms.TextInput(), required=False)
    is_user_manager = forms.BooleanField(label="Управление пользователями", widget=forms.CheckboxInput(), required=False)
    is_shop_manager = forms.BooleanField(label="Управление магазином", widget=forms.CheckboxInput(),
                                         required=False)
    is_event_manager = forms.BooleanField(label="Управление событиями", widget=forms.CheckboxInput(),
                                         required=False)

    class Meta:
        model = UserProfile
        fields = ['is_student', 'group', 'organization_name', 'image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_student') and cleaned_data.get('group') == '':
            raise ValidationError('У студента должен быть прописан номер группы')
        if not cleaned_data.get('is_student') and cleaned_data.get('organization_name') == '':
            raise ValidationError('Пользователь должен быть либо студентом, либо иметь организацию')




class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'autofocus': True}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


