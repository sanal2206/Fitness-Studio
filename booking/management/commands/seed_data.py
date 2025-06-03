from django.core.management.base import BaseCommand
from booking.models import FitnessClass
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed initial fitness class data'

    def handle(self, *args, **kwargs):
        FitnessClass.objects.all().delete()  # Clear existing data

        class_data = [
            {
                'name': 'Yoga',
                'datetime': make_aware(datetime.now() + timedelta(days=1, hours=8)),
                'instructor': 'Anita',
                'total_slots': 10,
                'available_slots': 10,
            },
            {
                'name': 'Zumba',
                'datetime': make_aware(datetime.now() + timedelta(days=2, hours=9)),
                'instructor': 'Raj',
                'total_slots': 15,
                'available_slots': 15,
            },
            {
                'name': 'HIIT',
                'datetime': make_aware(datetime.now() + timedelta(days=3, hours=10)),
                'instructor': 'Priya',
                'total_slots': 20,
                'available_slots': 20,
            },
        ]

        for class_item in class_data:
            FitnessClass.objects.create(**class_item)

        self.stdout.write(self.style.SUCCESS("Seeded fitness class data successfully!"))
