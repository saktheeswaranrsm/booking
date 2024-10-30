# Taxi Booking Web Application

This project is a taxi booking application built using Python and the Django framework. It provides a user-friendly interface for customers to book taxis, view booking details, modify or cancel bookings, and manage taxi availability.

## Features

- **Customer Booking**: Book taxis by selecting pickup and drop points, along with the pickup time.
- **Taxi Availability**: Taxis are assigned based on availability and location. Early morning bookings are handled with custom availability checks.
- **Dynamic Pricing**: Calculate fare based on distance between pickup and drop points.
- **Booking Modifications**: Modify existing bookings, including changing pickup and drop points and times.
- **Booking Cancellation**: Cancel bookings, with taxis updated for new availability.
- **Taxi Management**: Track the location, earnings, and future bookings of all taxis.

## Technologies Used

- **Backend**: Python, Django
- **Database**: SQLite3
- **Frontend**: HTML templates (Django template engine)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/taxi-booking-app.git
   cd taxi-booking-app