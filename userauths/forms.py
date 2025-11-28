from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

USER_TYPE = [
    ("Doctor", "Doctor"),
    ("Patient", "Patient"),
]

DEPARTMENT_CHOICES = [
    ("CSE", "Computer Science & Engineering"),
    ("EEE", "Electrical & Electronic Engineering"),
    ("ME", "Mechanical Engineering"),
    ("CE", "Civil Engineering"),
    ("BME", "Biomedical Engineering"),
    ("ETE", "Electronics & Telecommunication Engineering"),
    ("MME", "Materials and Metallurgical Engineering"),
    ("WRE", "Water Resources Engineering"),
    ("PME", "Petroleum & Mining Engineering"),
    ("ARCH", "Architecture"),
    ("URP", "Urban & Regional Planning"),

]

HALL_CHOICES = [
    ("Kazi Nazrul Islam Hall", "Kazi Nazrul Islam Hall"),
    ("Shaheed Shah Hall" , "Shaheed Shah hall" ),
    ("Shaheed Tarek Huda Hall", "Shahed Tarek Huda Hall"),
    ("Dr QK hall", "Dr QK hall"),
    ("Abu Sayed Hall", "Abu Sayed Hall"),
    ("MJH Hall", "MJH Hall"),
    ("Sufia kamal Hall", "Sufia kamal Hall"),
    ("Shamsen Nahar Hall", "Shamsen Nahar Hall"),
    ("Tapashi Rabeya Hall", "Tapashi Rabeya Hall"),
]

BLOOD_GROUP_CHOICES = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
]

class PatientRegistrationForm(UserCreationForm):
    # Student Information
    student_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2104096'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ashraful'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Islam'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2104096@student.cuet.ac.bd'})
    )
    
    # CUET Information
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    hall = forms.ChoiceField(
        choices=HALL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    room_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'S-401'})
    )
    
    # Personal Information
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01XXXXXXXXX'})
    )
    gender = forms.ChoiceField(
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'})
    )

    class Meta:
        model = User
        fields = ['student_id', 'first_name', 'last_name', 'email', 'department', 'hall', 
                 'room_no', 'mobile', 'gender', 'dob', 'blood_group', 'password1', 'password2']

class DoctorRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. John Doe'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dr.john@cuet.ac.bd'})
    )
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01XXXXXXXXX'})
    )
    specialization = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cardiology'})
    )
    qualifications = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MBBS, MD'})
    )
    years_of_experience = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5'})
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'mobile', 'specialization', 'qualifications', 
                 'years_of_experience', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@gmail.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'})
    )

    class Meta:
        model = User
        fields = ['email', 'password']