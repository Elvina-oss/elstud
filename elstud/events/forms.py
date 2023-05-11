from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['tittle', 'address', 'type', 'image', 'time', 'description']
