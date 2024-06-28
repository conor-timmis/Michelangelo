from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

# Create your models here.

#TIME_CHOICES = (

#('12:00', '12:00'),
#('13:00', '13:00'),
#('14:00', '14:00'),

#)

class Booking(models.Model):

    name = models.ForeignKey(User, on_delete=models.CASCADE)
    special_occasion = models.CharField(max_length=11, choices=[('Anniversary', 'anniversary'), ('Date', 'date'), ('Business', 'business')])
    meal_day = models.DateField()
    meal_time = models.TimeField()    
    number_of_guests = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )    
    customer_name = models.CharField(max_length=50)



    def clean(self):
        if self.meal_day and self.meal_day < now().date():
            raise ValidationError("Sorry, you cannot make a booking in the past.")

        existing_bookings = Booking.objects.filter(meal_time=self.meal_time, meal_day=self.meal_day)
        if self.pk:
            existing_bookings = existing_bookings.exclude(pk=self.pk)
        if existing_bookings.exists():
            raise ValidationError("Sorry, a booking already exists at this time on this day.")