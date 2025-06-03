import pytz
from django.utils import timezone
from rest_framework import serializers
from .models import Booking, FitnessClass

class FitnessClassSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = '__all__'

    def get_datetime(self, obj):
        request = self.context.get('request')
        tz_name = request.query_params.get('timezone', 'Asia/Kolkata') if request else 'Asia/Kolkata'
        try:
            user_tz = pytz.timezone(tz_name)
        except Exception:
            user_tz = pytz.timezone('Asia/Kolkata')
        dt_user_tz = timezone.localtime(obj.datetime, user_tz)
        return dt_user_tz.strftime("%Y-%m-%d %H:%M:%S %Z")

    def validate_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Class datetime cannot be in the past.")
        return value

    def validate_available_slots(self, value):
        if value < 0:
            raise serializers.ValidationError("Available slots cannot be negative.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)
    booked_at = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'

    def get_booked_at(self, obj):
        request = self.context.get('request')
        tz_name = request.query_params.get('timezone', 'Asia/Kolkata') if request else 'Asia/Kolkata'
        try:
            user_tz = pytz.timezone(tz_name)
        except Exception:
            user_tz = pytz.timezone('Asia/Kolkata')
        dt_user_tz = timezone.localtime(obj.booked_at, user_tz)
        return dt_user_tz.strftime("%Y-%m-%d %H:%M:%S %Z")
    

    def validate_client_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate(self, data):
        fitness_class = data.get('fitness_class')
        if fitness_class and fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No available slots for this class.")
        return data
