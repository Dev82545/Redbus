from django.contrib import admin
from .models import buses, Seat_booked, stop

class BusAdmin(admin.ModelAdmin):
    filter_horizontal = ('stop',)  # This will render a horizontal filter widget for the stops field


admin.site.register(buses, BusAdmin)
admin.site.register(Seat_booked)
admin.site.register(stop)

# Register your models here.
