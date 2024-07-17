from django import forms
from django.db import models
from django.conf import settings

# Create your models here.

# Represents a booking made by a user and indicates if the table is booked.
class Booking(models.Model):
    SPECIAL_OCCASIONS = (
        ('Bday', 'Birthday'),
        ('Anv.', 'Anniversary'),
        ('Other', 'Other'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    special_occasion = models.CharField(max_length=20, choices=SPECIAL_OCCASIONS)
    meal_day = models.DateField()
    meal_time = models.TimeField()
    number_of_guests = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    is_booked = models.BooleanField(default=False)

    # Meta class to set (with constraints) how to register a booking.
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'meal_day', 'meal_time', 'special_occasion'], name='unique_booking')
        ]
