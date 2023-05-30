from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'type', 'image', 'time_start', 'time_end', 'description', 'address', 'latitude', 'longitude']
        widgets = {
            'address': forms.HiddenInput(),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput()
        }

