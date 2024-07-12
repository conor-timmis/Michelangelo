from django import forms
from django.db import models
from django.conf import settings

# Create your models here.

class Booking(models.Model):
    SPECIAL_OCCASIONS = (
        ('BD', 'Birthday'),
        ('AN', 'Anniversary'),
        ('OT', 'Other'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    special_occasion = models.CharField(max_length=20, choices=SPECIAL_OCCASIONS)
    meal_day = models.DateField()
    meal_time = models.TimeField()
    number_of_guests = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    is_booked = models.BooleanField(default=False)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['special_occasion', 'meal_day', 'meal_time', 'number_of_guests', 'customer_name', 'is_booked']
        widgets = {
            'meal_day': forms.DateInput(attrs={'class': 'datepicker'}),
            'meal_time': forms.TimeInput(format='%H:%M'),
        }
