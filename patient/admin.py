from django.contrib import admin
from patient import models

class PatientAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'department', 'hall', 'room_no', 'mobile', 'gender']
    search_fields = ['student_id', 'first_name', 'last_name', 'email', 'department']
    list_filter = ['department', 'hall', 'gender', 'blood_group']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'student_id', 'first_name', 'last_name', 'email')
        }),
        ('CUET Information', {
            'fields': ('department', 'hall', 'room_no')
        }),
        ('Personal Information', {
            'fields': ('mobile', 'address', 'gender', 'dob', 'blood_group', 'image')
        }),
    )

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'type', 'seen', 'date']

admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Notification, NotificationAdmin)