from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Taxi(models.Model):
    taxi_id = models.IntegerField(unique=True)
    current_location = models.CharField(max_length=1, default='A')
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Taxi-{self.taxi_id}"

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=1)
    drop_point = models.CharField(max_length=1)
    pickup_time = models.DateTimeField()
    drop_time = models.DateTimeField()
    booking_time = models.TimeField(auto_now_add=True)
    booking_date = models.DateField(auto_now_add=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking {self.id} - {self.customer.name}"

