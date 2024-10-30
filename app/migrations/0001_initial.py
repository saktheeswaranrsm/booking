# Generated by Django 5.0.7 on 2024-07-25 17:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Taxi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxi_id', models.IntegerField(unique=True)),
                ('current_location', models.CharField(default='A', max_length=1)),
                ('earnings', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_point', models.CharField(max_length=1)),
                ('drop_point', models.CharField(max_length=1)),
                ('pickup_time', models.IntegerField()),
                ('drop_time', models.IntegerField()),
                ('booking_time', models.TimeField(auto_now_add=True)),
                ('booking_date', models.DateField(auto_now_add=True)),
                ('fare', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
                ('taxi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.taxi')),
            ],
        ),
    ]