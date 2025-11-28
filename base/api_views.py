# base/api_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from base import models as base_models
from doctor import models as doctor_models

@extend_schema(
    summary="Get all services",
    description="Retrieve list of all available medical services",
    responses={
        200: OpenApiTypes.OBJECT,
    },
    tags=['Services']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_services(request):
    services = base_models.Service.objects.all()
    data = [
        {
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': str(service.price) if service.price else None,
        }
        for service in services
    ]
    return Response({'services': data})

@extend_schema(
    summary="Get available doctors",
    description="Retrieve doctors with available slots",
    parameters=[
        OpenApiParameter(
            name='date', 
            description='Filter by date (YYYY-MM-DD)', 
            required=False, 
            type=OpenApiTypes.DATE
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
    },
    tags=['Doctors']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_doctors_available(request):
    from datetime import date
    today = date.today()
    
    available_doctors = doctor_models.Doctor.objects.filter(
        doctoravailableslot__date=today,
        doctoravailableslot__is_booked=False
    ).distinct()
    
    data = []
    for doctor in available_doctors:
        available_slots = doctor.doctoravailableslot_set.filter(
            date=today, 
            is_booked=False
        ).order_by('start_time')
        
        data.append({
            'doctor_id': doctor.id,
            'full_name': doctor.full_name,
            'specialization': doctor.specialization,
            'available_slots': [
                {
                    'slot_id': slot.id,
                    'date': slot.date,
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M'),
                }
                for slot in available_slots
            ]
        })
    
    return Response({'doctors': data, 'date': today})