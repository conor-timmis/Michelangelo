from datetime import datetime, time
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from zoneinfo import ZoneInfo
from .models import Booking, Review


# Define the form for a booking
class BookingForm(forms.ModelForm):

    MEAL_TIME_CHOICES = [
        (
            time(hour=h, minute=m).strftime('%H:%M'),
            time(hour=h, minute=m).strftime('%H:%M')
        )
        for h in range(14, 21)
        for m in range(0, 60, 15)
        if not (h == 20 and m > 0)
    ]
    meal_time = forms.ChoiceField(choices=MEAL_TIME_CHOICES)

    NUMBER_OF_GUESTS_CHOICES = [(i, str(i)) for i in range(1, 17)]
    number_of_guests = forms.ChoiceField(choices=NUMBER_OF_GUESTS_CHOICES)

    # Meta class for additional options
    class Meta:
        model = Booking
        widgets = {'meal_day': forms.DateInput(attrs={'class': 'datepicker'})}
        fields = [
            'special_occasion', 'meal_day', 'meal_time',
            'number_of_guests', 'customer_name'
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'meal_day', 'meal_time', 'special_occasion'],
                name='unique_booking'
            )
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

        # If either meal_day or meal_time is None, return early
        if meal_day is None or meal_time is None:
            return cleaned_data

        # Use of my personal time zone to stop the booking of tables
        # before the current time (in the United Kingdom)
        restaurant_tz = ZoneInfo('Europe/London')
        now = datetime.now(restaurant_tz)
        now = now.replace(second=0, microsecond=0)

        meal_datetime = datetime.combine(
            meal_day, meal_time, tzinfo=restaurant_tz
        )

        if meal_datetime < now:
            raise ValidationError(
                "The booking date or time cannot be in the past!"
            )

        try:
            self.instance.clean()
        except ValidationError as e:
            self.add_error(None, e.message)
            if 'meal_time' in e.message_dict:
                self.fields['meal_time'].widget.attrs.update(
                    {'class': 'meal-time taken'}
                )

        return cleaned_data


# The Review form setup for the booking view page
class ReviewForm(forms.ModelForm):
    booking = forms.ModelChoiceField(queryset=Booking.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['booking'].queryset = Booking.objects.filter(user=user)

    class Meta:
        model = Review
        fields = ['booking', 'comment']
