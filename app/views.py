from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .models import Customer, Taxi, Booking
from .forms import BookingForm, ModifyBookingForm
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Customer, Taxi, Booking
from .forms import BookingForm
from django.db.models import Min
from datetime import timedelta
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q



points = ['A', 'B', 'C', 'D', 'E', 'F']

def index(request):
    return render(request, 'index.html')

 
def calculate_travel_time(point1, point2):
    return abs(points.index(point1) - points.index(point2))
    return 1

def calculate_amount(pickup_point, drop_point):
    pickup_index = points.index(pickup_point)
    drop_index = points.index(drop_point)
    distance = abs(drop_index - pickup_index) * 15
    if distance <= 5:
        fare = 100
    else:
        fare = 100 + (distance - 5) * 10
    return fare

from django.utils import timezone

def reset_taxi_locations():
    current_time = timezone.now()
    if current_time.hour == 0 and current_time.minute == 0:
        for taxi in Taxi.objects.all():
            taxi.current_location = 'A'
            taxi.save()
        print("All taxis have been relocated to point A for the new day.")


def book_taxi(request):
    reset_taxi_locations()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            pickup_point = form.cleaned_data['pickup_point']
            drop_point = form.cleaned_data['drop_point']
            pickup_datetime = form.cleaned_data['pickup_datetime']
            
            if pickup_point == drop_point:
                messages.error(request, "Pickup and drop points cannot be the same. Please choose different points.")
                return render(request, 'book_taxi.html', {'form': form})
        
            customer, created = Customer.objects.get_or_create(name=customer_name)
            
            distance = abs(ord(drop_point) - ord(pickup_point))
            drop_time = pickup_datetime + timedelta(hours=distance)
            
            # Check if it's an early morning booking (between midnight and 6 AM)
            is_early_morning = 0 <= pickup_datetime.hour < 6
            
            if is_early_morning:
                available_taxi_info = find_taxi_for_early_morning(pickup_point, drop_point, pickup_datetime, drop_time)
            else:
                available_taxi_info = find_available_taxi(pickup_point, drop_point, pickup_datetime, drop_time)
            
            if available_taxi_info:
                available_taxi, earliest_pickup_time = available_taxi_info
                distance_km = distance * 15 
                if distance_km <= 5:
                    fare = 100
                else:
                    fare = 100 + (distance_km - 5) * 10
                
                actual_pickup_time = max(pickup_datetime, earliest_pickup_time)
                actual_drop_time = actual_pickup_time + timedelta(hours=distance)
                
                booking = Booking.objects.create(
                    customer=customer,
                    taxi=available_taxi,
                    pickup_point=pickup_point,
                    drop_point=drop_point,
                    pickup_time=actual_pickup_time,
                    drop_time=actual_drop_time,
                    fare=fare
                )
                
                available_taxi.current_location = drop_point
                available_taxi.earnings += fare
                available_taxi.save()
                
                if actual_pickup_time > pickup_datetime:
                    messages.warning(request, f"The taxi will arrive at {actual_pickup_time.strftime('%I:%M %p')}. Please be ready at the pickup point.")
                
                return redirect('booking_details', booking_id=booking.id)
            else:
                messages.error(request, "No taxis available at the moment. Please try again later.")
                return render(request, 'book_taxi.html', {'form': form})
    else:
        form = BookingForm()
    
    return render(request, 'book_taxi.html', {'form': form})

def is_taxi_available(taxi, pickup_point, drop_point, pickup_time, drop_time):
    conflicting_bookings = Booking.objects.filter(
        taxi=taxi,
        pickup_time__lt=drop_time,
        drop_time__gt=pickup_time
    )
    if conflicting_bookings.exists():
        return False
 
    last_booking = Booking.objects.filter(
        taxi=taxi,
        drop_time__lte=pickup_time
    ).order_by('-drop_time').first()

    if last_booking:
        time_to_reach_pickup = calculate_travel_time(last_booking.drop_point, pickup_point)
        if last_booking.drop_time + timezone.timedelta(hours=time_to_reach_pickup) > pickup_time:
            return False

    return True

def find_available_taxi(pickup_point, drop_point, pickup_time, drop_time):
    all_taxis = Taxi.objects.all()
    available_taxis = []

    for taxi in all_taxis:
        last_booking = Booking.objects.filter(
            taxi=taxi,
            drop_time__lte=pickup_time
        ).order_by('-drop_time').first()

        if last_booking:
            taxi_start_point = last_booking.drop_point
            taxi_start_time = last_booking.drop_time
        else:
            taxi_start_point = taxi.current_location
            taxi_start_time = timezone.now()

        time_to_reach = calculate_travel_time(taxi_start_point, pickup_point)
        taxi_available_time = taxi_start_time + timezone.timedelta(hours=time_to_reach)

        if taxi_available_time <= pickup_time:
            conflicting_bookings = Booking.objects.filter(
                taxi=taxi
            ).filter(
                Q(pickup_time__lt=drop_time, drop_time__gt=pickup_time) |  
                Q(pickup_time__gt=pickup_time, pickup_time__lt=drop_time)  
            )

            if not conflicting_bookings.exists():
                available_taxis.append((taxi, taxi_available_time))

    if available_taxis:
        sorted_taxis = sorted(available_taxis, key=lambda x: (x[1], x[0].earnings))
        return sorted_taxis[0]
    else:
        return None

def find_taxi_for_early_morning(pickup_point, drop_point, pickup_time, drop_time):
    all_taxis = Taxi.objects.all()
    available_taxis = []

    for taxi in all_taxis:
        
        taxi_start_point = 'A'
        taxi_start_time = pickup_time.replace(hour=0, minute=0, second=0, microsecond=0)

      
        time_to_reach = calculate_travel_time(taxi_start_point, pickup_point)
        taxi_available_time = taxi_start_time + timezone.timedelta(hours=time_to_reach)

        if taxi_available_time <= pickup_time:
            conflicting_bookings = Booking.objects.filter(
                taxi=taxi
            ).filter(
                Q(pickup_time__lt=drop_time, drop_time__gt=pickup_time) |  
                Q(pickup_time__gt=pickup_time, pickup_time__lt=drop_time)  
            )

            if not conflicting_bookings.exists():
                available_taxis.append((taxi, taxi_available_time))

    if available_taxis:
      
        sorted_taxis = sorted(available_taxis, key=lambda x: (x[1], x[0].earnings))
        return sorted_taxis[0]
    else:
        return None


def booking_details(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'booking_details.html', {'booking': booking})

def taxi_details(request):
    taxis = Taxi.objects.all()
    current_time=timezone.now()

    for taxi in taxis:
        taxi.future_bookings = Booking.objects.filter(
            taxi=taxi,
            drop_time__gt=current_time
        ).order_by('pickup_time')

    return render(request, 'taxi_details.html', {'taxis': taxis,})


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        taxi = booking.taxi
        fare_amount = booking.fare

        taxi.earnings -= fare_amount
        taxi.save()
        
        booking.delete()
        
        remaining_bookings = Booking.objects.filter(taxi=taxi).order_by('pickup_time')
        if not remaining_bookings.exists():
            taxi.current_location = 'A'
        else:
            last_booking = remaining_bookings.last()
            taxi.current_location = last_booking.drop_point
        
        taxi.save()
        
        
        return redirect('taxi_details')
    
    return render(request, 'cancel_booking.html', {'booking': booking})

def modify_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    old_taxi = booking.taxi
    old_fare = booking.fare
    
    if request.method == 'POST':
        form = ModifyBookingForm(request.POST)
        if form.is_valid():
            
            new_pickup_point = form.cleaned_data['pickup_point']
            new_drop_point = form.cleaned_data['drop_point']
            new_pickup_datetime = form.cleaned_data['pickup_datetime']
            
            if new_pickup_point == new_drop_point:
                messages.error(request, "Pickup and drop points cannot be the same. Please choose different points.")
                return render(request, 'modify_booking.html', {'form': form, 'booking': booking})
            
            distance = abs(points.index(new_pickup_point) - points.index(new_drop_point))
            new_drop_time = new_pickup_datetime + timezone.timedelta(hours=distance)
            
            new_fare = calculate_amount(new_pickup_point, new_drop_point)
            
            current_taxi_available = is_taxi_available(old_taxi, new_pickup_point, new_drop_point, new_pickup_datetime, new_drop_time)
            
            if current_taxi_available:
                assigned_taxi = old_taxi
            else:
                assigned_taxi = find_available_taxi(new_pickup_point, new_drop_point, new_pickup_datetime, new_drop_time)
            
            if assigned_taxi:
                if isinstance(assigned_taxi, tuple):
                    assigned_taxi = assigned_taxi[0]
                booking.taxi = assigned_taxi
                booking.pickup_point = new_pickup_point
                booking.drop_point = new_drop_point
                booking.pickup_time = new_pickup_datetime
                booking.drop_time = new_drop_time
                booking.fare = new_fare
                booking.save()
                
                assigned_taxi.current_location = new_drop_point
                assigned_taxi.earnings += new_fare
                assigned_taxi.save()
                
                if old_taxi != assigned_taxi:
                    old_taxi.earnings = max(0, old_taxi.earnings - old_fare)
                    old_taxi.save()
                else:
                    assigned_taxi.earnings = max(0, assigned_taxi.earnings - old_fare + new_fare)
                    assigned_taxi.save()
                
                return redirect('booking_details',booking_id=booking.id)
            else:
                messages.error(request, "No taxis are available for the new time slot. Please choose a different time.")
        else:
            messages.error(request, "Invalid form data. Please check your inputs.")
    else:
        form = ModifyBookingForm(initial={
           
            'pickup_point': booking.pickup_point,
            'drop_point': booking.drop_point,
            'pickup_datetime': booking.pickup_time
        })
    
    return render(request, 'modify_booking.html', {'form': form, 'booking': booking})