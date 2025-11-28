from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from doctor import models as doctor_models
from base import models as base_models
from datetime import date


@login_required
def dashboard(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(
        doctor=doctor
    ).exclude(
        status='Completed'  # Exclude completed appointments
    ).order_by(
        'created_at'  # Sort by earliest booking first
    )
    notifications = doctor_models.Notification.objects.filter(doctor=doctor, seen=False)

    context = {
        "appointments": appointments,
        "notifications": notifications,
    }
    return render(request, "doctor/dashboard.html", context)


@login_required
def appointments(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(
        doctor=doctor
    ).exclude(
        status='Completed'  # Exclude completed appointments
    ).order_by(
        'created_at'  # Sort by earliest booking first
    )

    return render(request, "doctor/appointments.html", {"appointments": appointments})


@login_required
def appointment_detail(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    return render(request, "doctor/appointment_detail.html", {
        "appointment": appointment,
        "medical_records": medical_records,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
    })


# -----------------------------
# LOGIC UPDATED HERE (Cancel frees slot)
# -----------------------------
@login_required
def cancel_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)

    appointment.status = "Cancelled"
    appointment.save()

    # FREE THE SLOT
    if appointment.slot:
        appointment.slot.is_booked = False
        appointment.slot.save()

    messages.success(request, "Appointment Cancelled Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)

    appointment.status = "Scheduled"
    appointment.save()

    messages.success(request, "Appointment Re-Scheduled Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


# -----------------------------
# LOGIC UPDATED HERE (Complete frees slot)
# -----------------------------
@login_required
def complete_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)

    appointment.status = "Completed"
    appointment.save()

    # FREE SLOT WHEN COMPLETED
    if appointment.slot:
        appointment.slot.is_booked = False
        appointment.slot.save()

    messages.success(request, "Appointment Completed Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def add_medical_report(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)

    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        base_models.MedicalRecord.objects.create(
            appointment=appointment,
            diagnosis=diagnosis,
            treatment=treatment
        )

    messages.success(request, "Medical Report Added Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def edit_medical_report(request, appointment_id, medical_report_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_report = base_models.MedicalRecord.objects.get(id=medical_report_id, appointment=appointment)

    if request.method == "POST":
        medical_report.diagnosis = request.POST.get("diagnosis")
        medical_report.treatment = request.POST.get("treatment")
        medical_report.save()

    messages.success(request, "Medical Report Updated Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def add_lab_test(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)

    if request.method == "POST":
        base_models.LabTest.objects.create(
            appointment=appointment,
            test_name=request.POST.get("test_name"),
            description=request.POST.get("description"),
            result=request.POST.get("result")
        )

    messages.success(request, "Lab Report Added Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def edit_lab_test(request, appointment_id, lab_test_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    lab_test = base_models.LabTest.objects.get(id=lab_test_id, appointment=appointment)

    if request.method == "POST":
        lab_test.test_name = request.POST.get("test_name")
        lab_test.description = request.POST.get("description")
        lab_test.result = request.POST.get("result")
        lab_test.save()

    messages.success(request, "Lab Report Updated Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def add_prescription(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)

    if request.method == "POST":
        base_models.Prescription.objects.create(
            appointment=appointment,
            medications=request.POST.get("medications")
        )

    messages.success(request, "Prescription Added Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def edit_prescription(request, appointment_id, prescription_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    prescription = base_models.Prescription.objects.get(id=prescription_id)

    if request.method == "POST":
        prescription.medications = request.POST.get("medications")
        prescription.save()

    messages.success(request, "Prescription Updated Successfully")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def payments(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(appointment__doctor=doctor, status="Paid")

    return render(request, "doctor/payments.html", {"payments": payments})


@login_required
def notifications(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    notifications = doctor_models.Notification.objects.filter(doctor=doctor, seen=False)

    return render(request, "doctor/notifications.html", {"notifications": notifications})


@login_required
def mark_noti_seen(request, id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    notification = doctor_models.Notification.objects.get(doctor=doctor, id=id)

    notification.seen = True
    notification.save()
    
    messages.success(request, "Notification marked as seen")
    return redirect("doctor:notifications")


@login_required
def profile(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    formatted_next_available_appointment_date = doctor.next_available_appointment_date.strftime('%Y-%m-%d')

    if request.method == "POST":
        doctor.full_name = request.POST.get("full_name")
        doctor.mobile = request.POST.get("mobile")
        doctor.country = request.POST.get("country")
        doctor.bio = request.POST.get("bio")
        doctor.specialization = request.POST.get("specialization")
        doctor.qualifications = request.POST.get("qualifications")
        doctor.years_of_experience = request.POST.get("years_of_experience")
        doctor.next_available_appointment_date = request.POST.get("next_available_appointment_date")

        if request.FILES.get("image"):
            doctor.image = request.FILES.get("image")

        doctor.save()
        messages.success(request, "Profile updated successfully")
        return redirect("doctor:profile")

    return render(request, "doctor/profile.html", {
        "doctor": doctor,
        "formatted_next_available_appointment_date": formatted_next_available_appointment_date,
    })


def home(request):
    """
    Display doctors who have available slots for today
    """
    today = date.today()
    
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
        'doctors_with_slots': doctors_with_slots,
        'today': today,
    }
    
    return render(request, 'base/index.html', context)
