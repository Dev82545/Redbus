import uuid
from django.db import models
from home.models import passengers
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

DAY_CHOICES = (
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
)

class stop(models.Model):
      stop = models.CharField(max_length = 100)
      
      def __str__(self):
        return self.stop

class buses(models.Model):
      id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      name = models.CharField(max_length= 255)
      date = models.DateField(default= "2025-01-01")
      city1 = models.CharField(max_length=255)
      city2 = models.CharField(max_length=255)
      dep_time =models.CharField(max_length= 255)
      arr_time =models.CharField(max_length= 255)
      stop = models.ManyToManyField(stop)
      slug = models.SlugField(max_length= 255)
      is_booked = models.BooleanField(default=False)
      luxury_seats = models.PositiveIntegerField(default = 0)
      luxury_seats_cost = models.PositiveIntegerField(default = 0)
      sleeper_seats = models.PositiveIntegerField(default = 0)
      sleeper_seats_cost = models.PositiveIntegerField(default = 0)
      seats =models.PositiveIntegerField()
      seats_cost = models.PositiveIntegerField(default = 0)
      active_days = MultiSelectField(choices=DAY_CHOICES, max_length=100, blank=True, null=True)

    
      def __str__(self):
        return self.name

class Seat_booked(models.Model):
   buses = models.ForeignKey(buses, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   seat_number = models.IntegerField()
   lseat_number = models.IntegerField()
   sseat_number = models.IntegerField()
   passengers = models.ManyToManyField(passengers, blank=True)
   tseat_number = models.PositiveIntegerField(default = 0)
   final_available_seats = models.JSONField(null=True, blank=True)
   
   def __str__(self):
    return f"Booking by {self.user.username} for {self.buses.name}"
  

    


# Create your models here.
