# userauths/api_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    summary="User registration",
    description="Register as Patient or Doctor",
    request=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            'Patient Registration',
            value={
                'username': 'student123',
                'email': 'student@cuet.ac.bd',
                'password': 'securepassword',
                'user_type': 'Patient',
                'student_id': '2019331001',
                'first_name': 'John',
                'last_name': 'Doe',
                'department': 'CSE',
                'hall': 'Bangabandhu Hall',
                'room_no': '301',
                'mobile': '017XXXXXXXX',
                'gender': 'Male',
                'dob': '2000-01-01',
                'blood_group': 'A+'
            }
        ),
        OpenApiExample(
            'Doctor Registration', 
            value={
                'username': 'dr_smith',
                'email': 'dr.smith@hospital.com',
                'password': 'securepassword',
                'user_type': 'Doctor',
                'full_name': 'Dr. John Smith',
                'mobile': '017XXXXXXXX',
                'specialization': 'Cardiology',
                'qualifications': 'MBBS, MD',
                'years_of_experience': 10
            }
        )
    ],
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    # You can implement the registration logic here
    # For now, return a mock response
    return Response({
        'status': 'success',
        'message': 'Registration endpoint - implement your logic here',
        'user_type': request.data.get('user_type', 'Patient')
    }, status=status.HTTP_201_CREATED)

@extend_schema(
    summary="User login",
    description="Authenticate user and return session",
    request=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            'Login Example',
            value={
                'email': 'user@example.com',
                'password': 'password123'
            }
        )
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    # Implement login logic here
    return Response({
        'status': 'success', 
        'message': 'Login endpoint - implement your logic here'
    })