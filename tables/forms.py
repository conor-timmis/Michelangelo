from django.core.exceptions import ValidationError
from django import forms
from datetime import time, timedelta, datetime
from .models import Booking
from django.db import models
from django.utils import timezone
from zoneinfo import ZoneInfo
from .models import Review

# Define the form for a booking
class BookingForm(forms.ModelForm):
    meal_day = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    MEAL_TIME_CHOICES = [(time(hour=h, minute=m).strftime('%H:%M'), time(hour=h, minute=m).strftime('%H:%M')) for h in range(14, 21) for m in range(0, 60, 15) if not (h == 20 and m > 0)]
    meal_time = forms.ChoiceField(choices=MEAL_TIME_CHOICES)

    # Meta class for additional options
    class Meta:
        model = Booking
        fields = ['special_occasion', 'meal_day', 'meal_time', 'number_of_guests', 'customer_name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'meal_day', 'meal_time', 'special_occasion'], name='unique_booking')
        ]

    # This cleans the meal_time field
    def clean_meal_time(self):
        meal_time_str = self.cleaned_data.get('meal_time')
        if meal_time_str is not None:
            return datetime.strptime(meal_time_str, '%H:%M').time()
        else:
            return None

    # Clean all fields
    def clean(self):
        cleaned_data = super().clean()

        meal_day = cleaned_data.get('meal_day')
        meal_time = cleaned_data.get('meal_time')

        # Use of my personal time zone to stop the booking of tables before the current time (in the United Kingdom)
        restaurant_tz = ZoneInfo('Europe/London')
        now = datetime.now(restaurant_tz)
        now = now.replace(second=0, microsecond=0)

        meal_datetime = datetime.combine(meal_day, meal_time, tzinfo=restaurant_tz)

        if meal_datetime < now:
            raise ValidationError("The booking datetime cannot be in the past!")

        try:
            self.instance.clean()
        except ValidationError as e:
            self.add_error(None, e.message)
            if 'meal_time' in e.message_dict:
                self.fields['meal_time'].widget.attrs.update({'class': 'meal-time taken'})

        return cleaned_data

class ReviewForm(forms.ModelForm):
    booking = forms.ModelChoiceField(queryset=Booking.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['booking'].queryset = Booking.objects.filter(user=user)

    class Meta:
        model = Review
        fields = ['booking', 'rating', 'comment']
