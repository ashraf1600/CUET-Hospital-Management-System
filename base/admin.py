from django.contrib import admin
from base import models
from import_export.admin import ImportExportModelAdmin

# ---------- Inlines ----------
class AppointmentInline(admin.TabularInline):
    model = models.Appointment
    extra = 1

class MedicalRecordInline(admin.TabularInline):
    model = models.MedicalRecord
    extra = 1

class LabTestInline(admin.TabularInline):
    model = models.LabTest
    extra = 1

class PrescriptionInline(admin.TabularInline):
    model = models.Prescription
    extra = 1

# ---------- Admin Classes ----------
class ServiceAdmin(ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    filter_horizontal = ['available_doctors']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'get_slot', 'status']
    search_fields = ['patient__user__username', 'doctor__user__username']
    inlines = [MedicalRecordInline, LabTestInline, PrescriptionInline]  # Removed BillingInline

    # Display slot nicely in list view
    def get_slot(self, obj):
        if obj.slot:
            return f"{obj.slot.date} {obj.slot.start_time}-{obj.slot.end_time}"
        return "-"
    get_slot.short_description = "Appointment Slot"

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'diagnosis']

class LabTestAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'test_name']

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'medications']

# ---------- Register ----------
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Appointment, AppointmentAdmin)
admin.site.register(models.MedicalRecord, MedicalRecordAdmin)
admin.site.register(models.LabTest, LabTestAdmin)
admin.site.register(models.Prescription, PrescriptionAdmin)
# Billing removed for university hospital style
