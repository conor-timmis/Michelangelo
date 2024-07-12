# Generated by Django 4.2.1 on 2024-07-12 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('special_occasion', models.CharField(choices=[('BD', 'Birthday'), ('AN', 'Anniversary'), ('OT', 'Other')], max_length=20)),
                ('meal_day', models.DateField()),
                ('meal_time', models.TimeField()),
                ('number_of_guests', models.IntegerField()),
                ('customer_name', models.CharField(max_length=100)),
                ('is_booked', models.BooleanField(default=False)),
            ],
        ),
    ]
