from django.urls import path
from base import views

from .api_views import api_services, api_doctors_available

app_name = "base"

urlpatterns = [
    path('ai/suggestions/', views.ai_medical_suggestions, name='ai_suggestions'),
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("book-appointment/<service_id>/<doctor_id>/", views.book_appointment, name="book_appointment"),
    path('appointment-success/<str:appointment_id>/', views.appointment_success, name='appointment_success'),
    # path("chat/", views.chat_page, name="chat"),
    # path("ask-ai/", views.ask_ai, name="ask"),
    path("chat/", views.chat_page, name="chat_page"),
    path("ask-ai/", views.ask_ai, name="ask_ai"),
    path('medical-chat/', views.medical_chat, name='medical_chat'),
    path('ai/chat/', views.ai_chat_api, name='ai_chat'),


    
    # path("checkout/<billing_id>/", views.checkout, name="checkout"),
    # path("payment_status/<billing_id>/", views.payment_status, name="payment_status"),

    # path("stripe_payment/<billing_id>/", views.stripe_payment, name="stripe_payment"),
    # path("stripe_payment_verify/<billing_id>/", views.stripe_payment_verify, name="stripe_payment_verify"),
    # path("paypal_payment_verify/<billing_id>/", views.paypal_payment_verify, name="paypal_payment_verify"),

        # API endpoints
    path("api/services/", api_services, name="api_services"),
    path("api/doctors/available/", api_doctors_available, name="api_doctors_available"),

]