from django.urls import path
from doctor import views

app_name = "doctor"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # Appointment pages
    path("appointments/", views.appointments, name="appointments"),
    path("appointments/<str:appointment_id>/", views.appointment_detail, name="appointment_detail"),

    # Appointment actions
    path("cancel_appointment/<str:appointment_id>/", views.cancel_appointment, name="cancel_appointment"),
    path("activate_appointment/<str:appointment_id>/", views.activate_appointment, name="activate_appointment"),
    path("complete_appointment/<str:appointment_id>/", views.complete_appointment, name="complete_appointment"),

    # Medical Report
    path("add_medical_report/<str:appointment_id>/", views.add_medical_report, name="add_medical_report"),
    path("edit_medical_report/<str:appointment_id>/<str:medical_report_id>/",
         views.edit_medical_report, name="edit_medical_report"),

    # Lab Test
    path("add_lab_test/<str:appointment_id>/", views.add_lab_test, name="add_lab_test"),
    path("edit_lab_test/<str:appointment_id>/<str:lab_test_id>/",
         views.edit_lab_test, name="edit_lab_test"),

    # Prescription
    path("add_prescription/<str:appointment_id>/", views.add_prescription, name="add_prescription"),
    path("edit_prescription/<str:appointment_id>/<str:prescription_id>/",
         views.edit_prescription, name="edit_prescription"),

    # Payments
    path("payments/", views.payments, name="payments"),

    # Notifications
    path("notifications/", views.notifications, name="notifications"),
    path("mark_noti_seen/<int:id>/", views.mark_noti_seen, name="mark_noti_seen"),

    # Profile
    path("profile/", views.profile, name="profile"),
]
