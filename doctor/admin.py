from django.contrib import admin
from doctor import models

# ---------- Inlines ----------
class DoctorAvailableSlotInline(admin.TabularInline):
    model = models.DoctorAvailableSlot
    extra = 1
    fields = ['date', 'start_time', 'end_time', 'is_booked']
    readonly_fields = ['is_booked']  # optional: make booked status read-only

# ---------- Admin Classes ----------
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'specialization', 'qualifications', 'years_of_experience']
    search_fields = ['user__username', 'full_name', 'specialization']
    inlines = [DoctorAvailableSlotInline]  # Show slots inside doctor

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'date']
    list_filter = ['type', 'seen', 'date']
    search_fields = ['doctor__full_name', 'appointment__appointment_id']

class DoctorAvailableSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'is_booked']
    list_filter = ['doctor', 'date', 'is_booked']
    search_fields = ['doctor__full_name']

# ---------- Register ----------
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.DoctorAvailableSlot, DoctorAvailableSlotAdmin)
