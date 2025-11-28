from django.db import models
from shortuuid.django_fields import ShortUUIDField
from doctor import models as doctor_models
from patient import models as patient_models

# ----------------------
# Service Model
# ----------------------
class Service(models.Model):
    image = models.FileField(upload_to="images", null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    available_doctors = models.ManyToManyField(doctor_models.Doctor, blank=True)

    def __str__(self):
        return self.name

# ----------------------
# Appointment Model
# ----------------------
class Appointment(models.Model):
    STATUS = [
        ('Scheduled', 'Scheduled'), 
        ('Completed', 'Completed'), 
        ('Pending', 'Pending'), 
        ('Cancelled', 'Cancelled')
    ]
    
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_appointments')
    doctor = models.ForeignKey(doctor_models.Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointments')
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_patient')

    # Slot-based booking
    slot = models.ForeignKey(
        'doctor.DoctorAvailableSlot',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='slot_appointments'
    )

    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    status = models.CharField(max_length=120, choices=STATUS, default='Scheduled')
    
    # 🔹 NEW: Timestamp fields for sorting
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['created_at']  # Default ordering: earliest first

    def save(self, *args, **kwargs):
        # Automatically unmark slot if appointment is completed or cancelled
        if self.status in ["Completed", "Cancelled"] and self.slot and self.slot.is_booked:
            self.slot.is_booked = False
            self.slot.save()
        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.full_name} with {self.doctor.full_name}"

# ----------------------
# Medical Record
# ----------------------
class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record for {self.appointment.patient.full_name}"

# ----------------------
# Lab Test
# ----------------------
class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name

# ----------------------
# Prescription
# ----------------------
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medications = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.full_name}"