from django.core.exceptions import ValidationError
from django import forms
from datetime import time, timedelta, datetime
from .models import Booking
from django.db import models

class BookingForm(forms.ModelForm):
    meal_day = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    MEAL_TIME_CHOICES = [(time(hour=h, minute=m).strftime('%H:%M'), time(hour=h, minute=m).strftime('%H:%M')) for h in range(14, 21) for m in range(0, 60, 15) if not (h == 20 and m > 0)]
    meal_time = forms.ChoiceField(choices=MEAL_TIME_CHOICES)

    class Meta:
        model = Booking
        fields = ['special_occasion', 'meal_day', 'meal_time', 'number_of_guests', 'customer_name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'meal_day', 'meal_time', 'special_occasion'], name='unique_booking')
        ]

    def clean_meal_time(self):
        meal_time_str = self.cleaned_data.get('meal_time')
        if meal_time_str is not None:
            return datetime.strptime(meal_time_str, '%H:%M').time()
        else:
            return None

    def clean(self):
        cleaned_data = super().clean()

        try:
            self.instance.clean()
        except ValidationError as e:
            self.add_error(None, e.message)
            if 'meal_time' in e.message_dict:
                self.fields['meal_time'].widget.attrs.update({'class': 'meal-time taken'})

        return cleaned_data
