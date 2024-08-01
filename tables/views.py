from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from django.db import IntegrityError
from .forms import ReviewForm
from .models import Review

# Create your views here.


# To create a booking
@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            try:
                booking.save()
            except IntegrityError:
                form.add_error(None, 'You have already made this booking.')
                return render(request, 'create_booking.html', {'form': form})
            messages.success(request, 'Booking created successfully!')
            return redirect('table_list')
    else:
        form = BookingForm()
    return render(request, 'create_booking.html', {'form': form})


# To edit a booking
@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('table_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'edit_booking.html', {'form': form})


# To delete a booking
@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.success(request, 'Booking deleted successfully!')
    return redirect('table_list')


# To view the booking list both as a standard user or all of them as superuser
@login_required
def booking_list(request):
    if request.user.is_superuser:
        bookings = Booking.objects.filter(meal_day__lt=timezone.now().date())  # noqa
    else:
        bookings = Booking.objects.filter(user=request.user, meal_day__lt=timezone.now().date())  # noqa

    # How the review form is being handled
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted! Thank you.')
            return redirect('table_list')
        else:
            messages.error(request, 'There was an error with your submission.')
    else:
        form = ReviewForm(user=request.user)

    return render(request, 'table_list.html', {
        'form': form, 'bookings': bookings,
    })
