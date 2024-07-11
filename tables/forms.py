from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    meal_day = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    meal_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'meal-time'}))

    class Meta:
        model = Booking
        fields = ['special_occasion', 'meal_day', 'meal_time', 'number_of_guests', 'customer_name']

    def clean(self):
        cleaned_data = super().clean()

        try:
            self.instance.clean()
        except ValidationError as e:
            self.add_error(None, e.message)
            if 'meal_time' in e.message_dict:
                self.fields['meal_time'].widget.attrs.update({'class': 'meal-time taken'})

        return cleaned_data
