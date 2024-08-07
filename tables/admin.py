from django.contrib import admin
from .models import Booking, Review
from .forms import BookingForm

# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    form = BookingForm
    list_display = ('customer_name', 'meal_day', 'meal_time',
                    'number_of_guests', 'special_occasion')
    search_fields = ('customer_name',)
    list_filter = ('meal_day',)


admin.site.register(Booking, BookingAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'created_at')
    search_fields = ('user__username', 'booking__name', 'comment')


admin.site.register(Review, ReviewAdmin)
