from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from userauths import forms as userauths_forms
from doctor import models as doctor_models
from patient import models as patient_models
from userauths import models as userauths_models

def get_user_type_display(request):
    """Get user type from URL parameter with default as Patient"""
    user_type = request.GET.get('type', 'Patient')
    return user_type

def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")
    
    user_type = get_user_type_display(request)  # এই function ব্যবহার করা হচ্ছে
    
    if request.method == "POST":
        if user_type == "Patient":
            form = userauths_forms.PatientRegistrationForm(request.POST or None)
        else:
            form = userauths_forms.DoctorRegistrationForm(request.POST or None)

        if form.is_valid():
            # Create user account with pending status
            user = form.save(commit=False)
            user.user_type = user_type
            user.account_status = "Pending"  # Set to pending for admin verification
            user.save()
            
            if user_type == "Patient":
                # Create patient profile with all student information
                patient_models.Patient.objects.create(
                    user=user,
                    student_id=form.cleaned_data.get("student_id"),
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    email=form.cleaned_data.get("email"),
                    department=form.cleaned_data.get("department"),
                    hall=form.cleaned_data.get("hall"),
                    room_no=form.cleaned_data.get("room_no"),
                    mobile=form.cleaned_data.get("mobile"),
                    gender=form.cleaned_data.get("gender"),
                    dob=form.cleaned_data.get("dob"),
                    blood_group=form.cleaned_data.get("blood_group")
                )
                messages.success(request, "Student account created successfully! Waiting for admin verification.")
                
            else:  # Doctor
                doctor_models.Doctor.objects.create(
                    user=user,
                    full_name=form.cleaned_data.get("full_name"),
                    mobile=form.cleaned_data.get("mobile"),
                    specialization=form.cleaned_data.get("specialization"),
                    qualifications=form.cleaned_data.get("qualifications"),
                    years_of_experience=form.cleaned_data.get("years_of_experience")
                )
                messages.success(request, "Doctor account created successfully! Waiting for admin verification.")
            
            return redirect("userauths:sign-in")

    else:
        if user_type == "Patient":
            form = userauths_forms.PatientRegistrationForm()
        else:
            form = userauths_forms.DoctorRegistrationForm()

    context = {
        "form": form,
        "user_type": user_type  # context এ pass করা হচ্ছে
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")
    
    if request.method == "POST":
        form = userauths_forms.LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user_instance = userauths_models.User.objects.get(email=email, is_active=True)
                
                # Check if account is verified
                if user_instance.account_status == "Pending":
                    messages.error(request, "Your account is pending verification. Please wait for admin approval.")
                    return redirect("userauths:sign-in")
                
                elif user_instance.account_status == "Rejected":
                    messages.error(request, f"Your account was rejected. Reason: {user_instance.rejection_reason}")
                    return redirect("userauths:sign-in")
                
                user_authenticate = authenticate(request, email=email, password=password)

                if user_authenticate is not None:
                    login(request, user_authenticate)
                    messages.success(request, "Logged In successfully")
                    
                    next_url = request.GET.get("next", '/')
                    return redirect(next_url)
                else:
                    messages.error(request, "Invalid email or password!")
            except userauths_models.User.DoesNotExist:
                messages.error(request, "User does not exist!")
    else:
        form = userauths_forms.LoginForm()
    
    context = {
        "form": form
    }
    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("userauths:sign-in")