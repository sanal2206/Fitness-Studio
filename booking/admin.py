from django.contrib import admin
from .models import FitnessClass,Booking
# Register your models here.



@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'datetime', 'instructor', 'total_slots', 'available_slots')
    search_fields = ('name', 'instructor')
    list_filter = ('datetime',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'fitness_class', 'booked_at')
    search_fields = ('client_name', 'client_email')
    list_filter = ('booked_at', 'fitness_class')