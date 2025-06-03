from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from django.utils import timezone
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_classes(request):
    try:
        classes = FitnessClass.objects.filter(datetime__gte=timezone.now())
        if not classes.exists():
            return Response({'error': 'No upcoming classes available'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FitnessClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching classes: {e}")
        return Response({'error': 'Unable to fetch classes'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def book_class(request):
    class_id = request.data.get('class_id')
    name = request.data.get('client_name')
    email = request.data.get('client_email')

    if not all([class_id, name, email]):
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        fitness_class = FitnessClass.objects.get(id=class_id)
        if fitness_class.available_slots <= 0:
            logger.warning(f"No slots left for class ID: {class_id}")
            return Response({'error': 'No slots available'}, status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(fitness_class=fitness_class, client_name=name, client_email=email)
        fitness_class.available_slots -= 1
        fitness_class.save()
        logger.info(f"Booking confirmed for {email} in class {class_id}")
        return Response({'success': 'Booking Confirmed'}, status=status.HTTP_201_CREATED)

    except FitnessClass.DoesNotExist:
        logger.error(f"Invalid class ID: {class_id}")
        return Response({'error': 'Invalid class ID'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Unexpected error while booking: {e}")
        return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_booking(request):
    email = request.query_params.get('email')
    if not email:
        return Response({'error': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(client_email=email)
    serializer = BookingSerializer(bookings, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
