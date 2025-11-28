from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

from base import models as base_models
from patient import models as patient_models


@login_required
def dashboard(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Notification.objects.filter(patient=patient, seen=False)
    # total_spent = base_models.Billing.objects.filter(patient=patient).aggregate(total_spent = models.Sum("total"))['total_spent']
    
    context = {
        'appointments': appointments,
        'notifications': notifications,
        # 'total_spent': total_spent,
    }

    return render(request, "patient/dashboard.html", context)



@login_required
def appointments(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)

    context = {
        "appointments": appointments,
    }

    return render(request, "patient/appointments.html", context)


@login_required
def appointment_detail(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    context = {
        "appointment": appointment,
        "medical_records": medical_records,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
    }

    return render(request, "patient/appointment_detail.html", context)




@login_required
def cancel_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)

    appointment.status = "Cancelled"
    appointment.save()

    messages.success(request, "Appointment Cancelled Successfully")
    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)

    appointment.status = "Scheduled"
    appointment.save()

    messages.success(request, "Appointment Re-Scheduled Successfully")
    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)

    appointment.status = "Completed"
    appointment.save()

    messages.success(request, "Appointment Completed Successfully")
    return redirect("patient:appointment_detail", appointment.appointment_id)

@login_required
def payments(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(appointment__patient=patient, status="Paid")

    context = {
        "payments": payments,
    }

    return render(request, "patient/payments.html", context)


@login_required
def notifications(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    notifications = patient_models.Notification.objects.filter(patient=patient, seen=False)

    context = {
        "notifications": notifications
    }

    return render(request, "patient/notifications.html", context)

@login_required
def mark_noti_seen(request, id):
    patient = patient_models.Patient.objects.get(user=request.user)
    notification = patient_models.Notification.objects.get(patient=patient, id=id)
    notification.seen = True
    notification.save()
    
    messages.success(request, "Notification marked as seen")
    return redirect("patient:notifications")




@login_required
def profile(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    formatted_dob = patient.dob.strftime('%Y-%m-%d') if patient.dob else ''
    
    if request.method == "POST":
        # Student Information
        patient.first_name = request.POST.get("first_name")
        patient.last_name = request.POST.get("last_name")
        patient.hall = request.POST.get("hall")
        patient.room_no = request.POST.get("room_no")
        
        # Personal Information
        patient.mobile = request.POST.get("mobile")
        patient.address = request.POST.get("address")
        patient.gender = request.POST.get("gender")
        patient.dob = request.POST.get("dob")
        patient.blood_group = request.POST.get("blood_group")

        # Profile Image
        image = request.FILES.get("image")
        if image != None:
            patient.image = image

        patient.save()
        messages.success(request, "Profile updated successfully")
        return redirect("patient:profile")

    context = {
        "patient": patient,
        "formatted_dob": formatted_dob,
    }
    return render(request, "patient/profile.html", context)

@login_required
def e_booklet(request):
    """E-Booklet - All completed appointment records in one place"""
    patient = patient_models.Patient.objects.get(user=request.user)
    
    # শুধু completed appointments নিবে
    completed_appointments = base_models.Appointment.objects.filter(
        patient=patient, 
        status="Completed"
    ).order_by("-id")
    
    context = {
        "completed_appointments": completed_appointments,
        "patient": patient,
    }
    return render(request, "patient/e_booklet.html", context)