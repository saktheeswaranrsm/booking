from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book_taxi, name='book_taxi'),
    path('booking/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('taxis/', views.taxi_details, name='taxi_details'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('modify/<int:booking_id>/', views.modify_booking, name='modify_booking'),
]