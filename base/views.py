from django.shortcuts import render, redirect
from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models
from django.contrib.auth.decorators import login_required
from datetime import date
from .wiki_qa import answer_question
from django.http import JsonResponse

from drf_spectacular.utils import extend_schema
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from django.views.decorators.csrf import csrf_exempt
from .ai_services import GeminiAIService
import datetime




@login_required
def medical_chat(request):
    context = {
        'current_time': timezone.now().strftime('%H:%M'),
    }
    return render(request, 'ai_chat/medical_chat.html', context)

@login_required
@csrf_exempt
def ai_chat_api(request):
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms', '')
        
        if not symptoms.strip():
            return JsonResponse({
                'success': False,
                'error': 'Please provide symptoms'
            })
        
        try:
            ai_service = GeminiAIService()
            response = ai_service.generate_medical_suggestions(symptoms)
            
            return JsonResponse({
                'success': True,
                'response': response
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def ai_medical_suggestions(request):
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms', '')
        history = request.POST.get('history', '')
        
        ai_service = GeminiAIService()
        suggestions = ai_service.generate_medical_suggestions(symptoms, history)
        
        return JsonResponse({'suggestions': suggestions})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def index(request):
    """
    Home page showing services and available doctors for today
    """
    today = date.today()
    
    # Get all services
    services = base_models.Service.objects.all()
    
    # Get all doctors who have available slots today
    available_doctors = doctor_models.Doctor.objects.filter(
        doctoravailableslot__date=today,
        doctoravailableslot__is_booked=False
    ).distinct().select_related('user')
    
    # For each doctor, get their available slots for today
    doctors_with_slots = []
    for doctor in available_doctors:
        available_slots = doctor_models.DoctorAvailableSlot.objects.filter(
            doctor=doctor,
            date=today,
            is_booked=False
        ).order_by('start_time')
        
        if available_slots.exists():
            doctors_with_slots.append({
                'doctor': doctor,
                'slots': available_slots,
                'slot_count': available_slots.count()
            })
    
    context = {
        'services': services,
        'doctors_with_slots': doctors_with_slots,
        'today': today,
    }
    
    return render(request, 'base/index.html', context)





def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)
    context = {
        "service": service
    }
    return render(request, "base/service_detail.html", context)


@login_required
def book_appointment(request, service_id, doctor_id):
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient = patient_models.Patient.objects.get(user=request.user)

    slots = doctor_models.DoctorAvailableSlot.objects.filter(
        doctor=doctor,
        is_booked=False
    ).order_by("date", "start_time")

    if request.method == "POST":
        # Update patient information with new fields
        patient.first_name = request.POST.get("first_name")
        patient.last_name = request.POST.get("last_name")
        patient.email = request.POST.get("email")
        patient.mobile = request.POST.get("mobile")
        patient.gender = request.POST.get("gender")
        patient.address = request.POST.get("address")
        patient.dob = request.POST.get("dob")
        patient.blood_group = request.POST.get("blood_group")
        patient.save()

        # Get selected slot
        slot_id = request.POST.get("slot_id")
        slot = doctor_models.DoctorAvailableSlot.objects.get(id=slot_id)

        # Mark slot as booked
        slot.is_booked = True
        slot.save()

        # Create appointment with slot
        appointment = base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            slot=slot,
            issues=request.POST.get("issues"),
            symptoms=request.POST.get("symptoms"),
            status="Scheduled"
        )

        # Notify doctor
        doctor_models.Notification.objects.create(
            doctor=doctor,
            appointment=appointment,
            type="New Appointment"
        )

        return redirect("base:appointment_success", appointment_id=appointment.appointment_id)

    return render(request, "base/book_appointment.html", {
        "service": service,
        "doctor": doctor,
        "patient": patient,
        "slots": slots
    })


def appointment_success(request, appointment_id):
    """Appointment success page after booking"""
    try:
        appointment = base_models.Appointment.objects.get(appointment_id=appointment_id)
        context = {
            "appointment": appointment,
            "appointment_id": appointment_id
        }
    except base_models.Appointment.DoesNotExist:
        context = {
            "appointment": None,
            "appointment_id": appointment_id
        }
    
    return render(request, "base/appointment_success.html", context)







def chat_page(request):
    return render(request, "AI/chat_voice_text.html")

@extend_schema(
    request=OpenApiTypes.OBJECT,
    examples=[
        {
            'question': 'What are the symptoms of fever?'
        }
    ],
    responses={
        200: OpenApiTypes.OBJECT,
    },
    description="Ask medical questions to AI assistant"
)

def ask_ai(request):
    if request.method == "POST":
        question = request.POST.get("question", "")
        result = answer_question(question)
        return JsonResponse(result)

