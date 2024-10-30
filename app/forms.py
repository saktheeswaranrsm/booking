from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    pickup_point = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')])
    drop_point = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')])
    pickup_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

class ModifyBookingForm(forms.Form):
    pickup_point = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')])
    drop_point = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')])
    pickup_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    def clean(self):
        cleaned_data = super().clean()
        pickup_point = cleaned_data.get('pickup_point')
        drop_point = cleaned_data.get('drop_point')
        pickup_datetime = cleaned_data.get('pickup_datetime')
        
        if pickup_point == drop_point:
            raise forms.ValidationError("Pickup and drop points cannot be the same.")
        
        if pickup_datetime and pickup_datetime < timezone.now():
            raise forms.ValidationError("Pickup time cannot be in the past.")
        
        return cleaned_data