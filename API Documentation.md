# CUET Hospital Management System API Documentation

**Version:** 1.0.0
**Last Updated:** November 2025
**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [Core Concepts](#core-concepts)
5. [API Reference](#api-reference)
   - [Authentication APIs](#authentication-apis)
   - [Public APIs](#public-apis)
   - [Patient APIs](#patient-apis)
   - [Doctor APIs](#doctor-apis)
6. [Error Handling](#error-handling)
7. [Status Codes](#status-codes)
8. [Changelog](#changelog)

---

## Overview

The Hospital Management System API provides a comprehensive solution for managing medical appointments, patient records, doctor schedules, and healthcare services. Built with Django, it offers session-based authentication and role-based access control for patients, doctors, and administrators.

### Key Features

- **Appointment Management**: Slot-based scheduling system
- **Medical Records**: Comprehensive patient history tracking
- **Lab Tests & Prescriptions**: Complete diagnostic and treatment documentation
- **Real-time Notifications**: Stay updated on appointment status
- **AI Chat Assistant**: Intelligent medical query support
- **E-Booklet**: Digital medical history for patients

### Base URL

```
Development: http://localhost:8000
Production: [To be configured]
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- Active session cookie for authenticated endpoints

### Quick Start

**1. Register a new user**

```bash
curl -X POST "http://localhost:8000/auth/sign-up/?type=Patient" \
  -d "username=johndoe" \
  -d "email=john@example.com" \
  -d "password=secure123" \
  -d "first_name=John" \
  -d "last_name=Doe" \
  -d "student_id=2021001" \
  -d "department=Computer Science" \
  -d "mobile=+8801712345678"
```

**2. Login**

```bash
curl -X POST "http://localhost:8000/auth/sign-in/" \
  -d "email=john@example.com" \
  -d "password=secure123" \
  -c cookies.txt
```

**3. Book an appointment**

```bash
curl -X POST "http://localhost:8000/book-appointment/1/5/" \
  -b cookies.txt \
  -d "first_name=John" \
  -d "email=john@example.com" \
  -d "slot_id=12" \
  -d "issues=Regular checkup"
```

---

## Authentication

The API uses **session-based authentication** with Django's built-in authentication system.

### Authentication Flow

```
┌─────────────┐
│   Sign Up   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│   Sign In   │─────►│ Session ID   │
└──────┬──────┘      └──────┬───────┘
       │                    │
       │     ┌──────────────┘
       ▼     ▼
┌─────────────────┐
│ Authenticated   │
│   Requests      │
└─────────────────┘
```

### Session Management

- Sessions expire after 2 weeks of inactivity
- Session ID stored in `sessionid` cookie
- CSRF protection enabled for all POST requests
- Secure and HttpOnly flags set in production

### Required Headers

For authenticated endpoints:

```
Cookie: sessionid=<your_session_id>
```

For POST requests:

```
Cookie: sessionid=<your_session_id>
X-CSRFToken: <csrf_token>
```

---

## Core Concepts

### User Roles

| Role              | Description                     | Access Level                                                 |
| ----------------- | ------------------------------- | ------------------------------------------------------------ |
| **Patient** | Students receiving medical care | Personal appointments, medical records, notifications        |
| **Doctor**  | Medical professionals           | Manage appointments, add diagnoses, prescriptions, lab tests |
| **Admin**   | System administrators           | Full system access, user management                          |

### Appointment Lifecycle

```
┌──────────┐
│ Pending  │ Initial state when appointment is created
└────┬─────┘
     │
     ▼
┌───────────┐
│ Scheduled │ Confirmed with assigned time slot
└────┬──────┘
     │
     ├──────────┐
     ▼          ▼
┌───────────┐  ┌───────────┐
│ Completed │  │ Cancelled │
└───────────┘  └───────────┘
```

### Status Transitions

- **Pending → Scheduled**: Automatic upon booking with available slot
- **Scheduled → Completed**: Doctor or patient marks as complete
- **Scheduled → Cancelled**: Either party cancels the appointment
- **Cancelled → Scheduled**: Patient can reactivate if slot available

### Slot Management

- Time slots are managed by doctors
- Each slot can hold one appointment
- Cancelled appointments free up slots automatically
- Slots have specific date and time ranges

---

## API Reference

### Authentication APIs

#### Register User

**Endpoint:** `POST /auth/sign-up/`

Register a new patient or doctor account.

**Query Parameters:**

| Parameter | Type   | Required | Default | Description                         |
| --------- | ------ | -------- | ------- | ----------------------------------- |
| type      | string | No       | Patient | User type:`Patient` or `Doctor` |

**Request Body (Patient):**

| Field       | Type   | Required | Description                | Example           |
| ----------- | ------ | -------- | -------------------------- | ----------------- |
| username    | string | Yes      | Unique username            | johndoe           |
| email       | string | Yes      | Valid email address        | john@example.com  |
| password    | string | Yes      | Minimum 8 characters       | SecurePass123     |
| student_id  | string | Yes      | Student ID number          | 2021001           |
| first_name  | string | Yes      | First name                 | John              |
| last_name   | string | Yes      | Last name                  | Doe               |
| department  | string | Yes      | Academic department        | Computer Science  |
| hall        | string | No       | Residence hall             | Hall A            |
| room_no     | string | No       | Room number                | 305               |
| mobile      | string | Yes      | Phone number               | +8801712345678    |
| gender      | string | Yes      | Gender                     | Male/Female/Other |
| dob         | date   | Yes      | Date of birth (YYYY-MM-DD) | 2000-01-15        |
| blood_group | string | No       | Blood group                | A+                |

**Request Body (Doctor):**

| Field               | Type    | Required | Description            | Example            |
| ------------------- | ------- | -------- | ---------------------- | ------------------ |
| username            | string  | Yes      | Unique username        | drsarah            |
| email               | string  | Yes      | Valid email address    | sarah@hospital.com |
| password            | string  | Yes      | Minimum 8 characters   | SecurePass123      |
| full_name           | string  | Yes      | Full name              | Dr. Sarah Johnson  |
| mobile              | string  | Yes      | Phone number           | +8801812345678     |
| specialization      | string  | Yes      | Medical specialization | Cardiology         |
| qualifications      | string  | Yes      | Medical qualifications | MD, MRCP           |
| years_of_experience | integer | Yes      | Years of practice      | 10                 |

**Example Request (Patient):**

```bash
curl -X POST "http://localhost:8000/auth/sign-up/?type=Patient" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe" \
  -d "email=john@example.com" \
  -d "password=SecurePass123" \
  -d "student_id=2021001" \
  -d "first_name=John" \
  -d "last_name=Doe" \
  -d "department=Computer Science" \
  -d "mobile=+8801712345678" \
  -d "gender=Male" \
  -d "dob=2000-01-15" \
  -d "blood_group=A+"
```

**Response:**

```
302 Found
Location: /auth/sign-in/
```

**Error Responses:**

| Status | Description                                    |
| ------ | ---------------------------------------------- |
| 400    | Invalid input data or duplicate username/email |
| 500    | Server error during registration               |

---

#### Login

**Endpoint:** `POST /auth/sign-in/`

Authenticate user and create session.

**Request Body:**

| Field    | Type   | Required | Description      |
| -------- | ------ | -------- | ---------------- |
| email    | string | Yes      | Registered email |
| password | string | Yes      | User password    |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/auth/sign-in/" \
  -c cookies.txt \
  -d "email=john@example.com" \
  -d "password=SecurePass123"
```

**Response:**

```
302 Found
Location: /
Set-Cookie: sessionid=abc123xyz; HttpOnly; Path=/
```

**Error Responses:**

| Status | Description               |
| ------ | ------------------------- |
| 401    | Invalid credentials       |
| 400    | Missing email or password |

---

#### Logout

**Endpoint:** `GET /auth/sign-out/`

Terminate user session.

**Authentication:** Required

**Example Request:**

```bash
curl -X GET "http://localhost:8000/auth/sign-out/" \
  -b cookies.txt
```

**Response:**

```
302 Found
Location: /auth/sign-in/
```

---

### Public APIs

#### Home Page

**Endpoint:** `GET /`

Displays available medical services and doctor schedules.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/"
```

**Response:** HTML page with services and available appointment slots

---

#### Service Details

**Endpoint:** `GET /service/<service_id>/`

Get detailed information about a specific medical service.

**Path Parameters:**

| Parameter  | Type    | Description        |
| ---------- | ------- | ------------------ |
| service_id | integer | Service identifier |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/service/1/"
```

**Response:** HTML page with service details, doctors, and pricing

---

#### Book Appointment

**Endpoint:** `GET, POST /book-appointment/<service_id>/<doctor_id>/`

Book an appointment with a specific doctor for a service.

**Path Parameters:**

| Parameter  | Type    | Description        |
| ---------- | ------- | ------------------ |
| service_id | integer | Service identifier |
| doctor_id  | integer | Doctor identifier  |

**Request Body (POST):**

| Field       | Type    | Required | Description          | Example             |
| ----------- | ------- | -------- | -------------------- | ------------------- |
| first_name  | string  | Yes      | Patient's first name | John                |
| last_name   | string  | Yes      | Patient's last name  | Doe                 |
| email       | string  | Yes      | Contact email        | john@example.com    |
| mobile      | string  | Yes      | Phone number         | +8801712345678      |
| gender      | string  | Yes      | Gender               | Male                |
| address     | string  | No       | Residential address  | 123 Main St         |
| dob         | date    | Yes      | Date of birth        | 2000-01-15          |
| blood_group | string  | No       | Blood group          | A+                  |
| slot_id     | integer | Yes      | Time slot ID         | 12                  |
| issues      | text    | Yes      | Medical concerns     | Chest pain          |
| symptoms    | text    | No       | Current symptoms     | Shortness of breath |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/book-appointment/1/5/" \
  -d "first_name=John" \
  -d "last_name=Doe" \
  -d "email=john@example.com" \
  -d "mobile=+8801712345678" \
  -d "gender=Male" \
  -d "dob=2000-01-15" \
  -d "slot_id=12" \
  -d "issues=Regular checkup"
```

**Response:**

```
302 Found
Location: /appointment-success/123/
```

**Error Responses:**

| Status | Description                      |
| ------ | -------------------------------- |
| 404    | Service or doctor not found      |
| 400    | Slot unavailable or invalid data |

---

#### Appointment Success

**Endpoint:** `GET /appointment-success/<appointment_id>/`

Display appointment confirmation details.

**Path Parameters:**

| Parameter      | Type    | Description            |
| -------------- | ------- | ---------------------- |
| appointment_id | integer | Appointment identifier |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/appointment-success/123/"
```

**Response:** HTML page with appointment confirmation

---

#### AI Chat Interface

**Endpoint:** `GET /chat/`

Access AI-powered medical chat assistant.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/chat/"
```

**Response:** HTML chat interface

---

#### Ask AI

**Endpoint:** `POST /ask-ai/`

Get AI-generated responses to medical queries.

**Request Body:**

| Field    | Type   | Required | Description      |
| -------- | ------ | -------- | ---------------- |
| question | string | Yes      | Medical question |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/ask-ai/" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the symptoms of flu?"}'
```

**Example Response:**

```json
{
  "answer": "Common flu symptoms include fever, cough, sore throat, body aches, headache, and fatigue. Symptoms typically appear 1-4 days after infection and last 5-7 days.",
  "status": "success"
}
```

---

### Patient APIs

All patient endpoints require authentication and patient role.

#### Patient Dashboard

**Endpoint:** `GET /patient/`

**Authentication:** Required (Patient)

Display patient dashboard with overview of appointments and notifications.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/" \
  -b cookies.txt
```

**Response:** HTML dashboard with appointments, notifications, and quick actions

---

#### Appointments List

**Endpoint:** `GET /patient/appointments`

**Authentication:** Required (Patient)

Get all appointments for the logged-in patient.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/appointments" \
  -b cookies.txt
```

**Response:** HTML page with filterable appointments list

---

#### Appointment Details

**Endpoint:** `GET /patient/appointments/<appointment_id>/`

**Authentication:** Required (Patient)

View detailed information about a specific appointment including medical records, lab tests, and prescriptions.

**Path Parameters:**

| Parameter      | Type    | Description            |
| -------------- | ------- | ---------------------- |
| appointment_id | integer | Appointment identifier |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/appointments/123/" \
  -b cookies.txt
```

**Response:** HTML page with complete appointment details

**Error Responses:**

| Status | Description                             |
| ------ | --------------------------------------- |
| 404    | Appointment not found                   |
| 403    | Not authorized to view this appointment |

---

#### Cancel Appointment

**Endpoint:** `GET /patient/cancel_appointment/<appointment_id>/`

**Authentication:** Required (Patient)

Cancel a scheduled appointment and free up the time slot.

**Path Parameters:**

| Parameter      | Type    | Description           |
| -------------- | ------- | --------------------- |
| appointment_id | integer | Appointment to cancel |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/cancel_appointment/123/" \
  -b cookies.txt
```

**Response:**

```
302 Found
Location: /patient/appointments/123/
```

---

#### Activate Appointment

**Endpoint:** `GET /patient/activate_appointment/<appointment_id>/`

**Authentication:** Required (Patient)

Reactivate a cancelled appointment if the slot is still available.

**Path Parameters:**

| Parameter      | Type    | Description             |
| -------------- | ------- | ----------------------- |
| appointment_id | integer | Appointment to activate |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/activate_appointment/123/" \
  -b cookies.txt
```

**Response:**

```
302 Found
Location: /patient/appointments/123/
```

**Error Responses:**

| Status | Description              |
| ------ | ------------------------ |
| 400    | Slot no longer available |

---

#### Complete Appointment

**Endpoint:** `GET /patient/complete_appointment/<appointment_id>/`

**Authentication:** Required (Patient)

Mark an appointment as completed from patient side.

**Path Parameters:**

| Parameter      | Type    | Description             |
| -------------- | ------- | ----------------------- |
| appointment_id | integer | Appointment to complete |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/complete_appointment/123/" \
  -b cookies.txt
```

**Response:**

```
302 Found
Location: /patient/appointments/123/
```

---

#### E-Booklet

**Endpoint:** `GET /patient/e-booklet/`

**Authentication:** Required (Patient)

View complete medical history with all completed appointments.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/e-booklet/" \
  -b cookies.txt
```

**Response:** HTML page with chronological medical history

---

#### Notifications

**Endpoint:** `GET /patient/notifications/`

**Authentication:** Required (Patient)

Get list of unread notifications.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/notifications/" \
  -b cookies.txt
```

**Response:** HTML page with notifications list

---

#### Mark Notification as Read

**Endpoint:** `GET /patient/mark_noti_seen/<id>/`

**Authentication:** Required (Patient)

Mark a specific notification as read.

**Path Parameters:**

| Parameter | Type    | Description             |
| --------- | ------- | ----------------------- |
| id        | integer | Notification identifier |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/patient/mark_noti_seen/45/" \
  -b cookies.txt
```

**Response:**

```
302 Found
Location: /patient/notifications/
```

---

#### Patient Profile

**Endpoint:** `GET, POST /patient/profile/`

**Authentication:** Required (Patient)

View and update patient profile information.

**Request Body (POST):**

| Field       | Type   | Required | Description     |
| ----------- | ------ | -------- | --------------- |
| first_name  | string | Yes      | First name      |
| last_name   | string | Yes      | Last name       |
| hall        | string | No       | Residence hall  |
| room_no     | string | No       | Room number     |
| mobile      | string | Yes      | Phone number    |
| address     | string | No       | Full address    |
| gender      | string | Yes      | Gender          |
| dob         | date   | Yes      | Date of birth   |
| blood_group | string | No       | Blood group     |
| image       | file   | No       | Profile picture |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/patient/profile/" \
  -b cookies.txt \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "mobile=+8801712345678" \
  -F "image=@profile.jpg"
```

**Response:** Updated profile page with success message

---

### Doctor APIs

All doctor endpoints require authentication and doctor role.

#### Doctor Dashboard

**Endpoint:** `GET /doctor/`

**Authentication:** Required (Doctor)

Display doctor dashboard with pending appointments overview.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/doctor/" \
  -b cookies.txt
```

**Response:** HTML dashboard with today's appointments and statistics

---

#### Doctor Appointments

**Endpoint:** `GET /doctor/appointments/`

**Authentication:** Required (Doctor)

Get all appointments for the logged-in doctor (excluding completed).

**Example Request:**

```bash
curl -X GET "http://localhost:8000/doctor/appointments/" \
  -b cookies.txt
```

**Response:** HTML page with appointments list

---

#### Appointment Details

**Endpoint:** `GET /doctor/appointments/<appointment_id>/`

**Authentication:** Required (Doctor)

View detailed appointment information with medical data entry forms.

**Path Parameters:**

| Parameter      | Type    | Description            |
| -------------- | ------- | ---------------------- |
| appointment_id | integer | Appointment identifier |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/doctor/appointments/123/" \
  -b cookies.txt
```

**Response:** HTML page with appointment details and medical forms

---

#### Cancel Appointment

**Endpoint:** `GET /doctor/cancel_appointment/<appointment_id>/`

**Authentication:** Required (Doctor)

Cancel appointment and automatically free the time slot.

**Path Parameters:**

| Parameter      | Type    | Description           |
| -------------- | ------- | --------------------- |
| appointment_id | integer | Appointment to cancel |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/doctor/cancel_appointment/123/" \
  -b cookies.txt
```

**Response:**

```
302 Found
Location: /doctor/appointments/123/
```

---

#### Complete Appointment

**Endpoint:** `GET /doctor/complete_appointment/<appointment_id>/`

**Authentication:** Required (Doctor)

Mark appointment as completed and free the time slot.

**Path Parameters:**

| Parameter      | Type    | Description             |
| -------------- | ------- | ----------------------- |
| appointment_id | integer | Appointment to complete |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/doctor/complete_appointment/123/" \
  -b cookies.txt
```

**Response:**

```
302 Found
Location: /doctor/appointments/123/
```

---

#### Add Medical Report

**Endpoint:** `POST /doctor/add_medical_report/<appointment_id>/`

**Authentication:** Required (Doctor)

Add medical diagnosis and treatment record to appointment.

**Path Parameters:**

| Parameter      | Type    | Description            |
| -------------- | ------- | ---------------------- |
| appointment_id | integer | Appointment identifier |

**Request Body:**

| Field     | Type | Required | Description       |
| --------- | ---- | -------- | ----------------- |
| diagnosis | text | Yes      | Medical diagnosis |
| treatment | text | Yes      | Treatment plan    |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/doctor/add_medical_report/123/" \
  -b cookies.txt \
  -d "diagnosis=Type 2 Diabetes Mellitus" \
  -d "treatment=Metformin 500mg twice daily, dietary modifications"
```

**Response:**

```
302 Found
Location: /doctor/appointments/123/
```

---

#### Edit Medical Report

**Endpoint:** `POST /doctor/edit_medical_report/<appointment_id>/<medical_report_id>/`

**Authentication:** Required (Doctor)

Update existing medical record.

**Path Parameters:**

| Parameter         | Type    | Description               |
| ----------------- | ------- | ------------------------- |
| appointment_id    | integer | Appointment identifier    |
| medical_report_id | integer | Medical report identifier |

**Request Body:**

| Field     | Type | Required | Description       |
| --------- | ---- | -------- | ----------------- |
| diagnosis | text | Yes      | Updated diagnosis |
| treatment | text | Yes      | Updated treatment |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/doctor/edit_medical_report/123/45/" \
  -b cookies.txt \
  -d "diagnosis=Type 2 Diabetes Mellitus - Well Controlled" \
  -d "treatment=Continue Metformin, add exercise regimen"
```

**Response:**

```
302 Found
Location: /doctor/appointments/123/
```

---

#### Add Lab Test

**Endpoint:** `POST /doctor/add_lab_test/<appointment_id>/`

**Authentication:** Required (Doctor)

Add laboratory test order and results.

**Path Parameters:**

| Parameter      | Type    | Description            |
| -------------- | ------- | ---------------------- |
| appointment_id | integer | Appointment identifier |

**Request Body:**

| Field       | Type   | Required | Description      |
| ----------- | ------ | -------- | ---------------- |
| test_name   | string | Yes      | Name of lab test |
| description | text   | No       | Test description |
| result      | text   | No       | Test results     |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/doctor/add_lab_test/123/" \
  -b cookies.txt \
  -d "test_name=HbA1c" \
  -d "description=Glycated hemoglobin test" \
  -d "result=6.5% - Borderline diabetic range"
```

**Response:**

```
302 Found
Location: /doctor/appointments/123/
```

---

#### Edit Lab Test

**Endpoint:** `POST /doctor/edit_lab_test/<appointment_id>/<lab_test_id>/`

**Authentication:** Required (Doctor)

Update existing lab test information.

**Path Parameters:**

| Parameter      | Type    | Description            |
| -------------- | ------- | ---------------------- |
| appointment_id | integer | Appointment identifier |
| lab_test_id    | integer | Lab test identifier    |

**Request Body:**

| Field       | Type   | Required | Description      |
| ----------- | ------ | -------- | ---------------- |
| test_name   | string | Yes      | Name of lab test |
| description | text   | No       | Test description |
| result      | text   | No       | Test results     |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/doctor/edit_lab_test/123/67/" \
  -b cookies.txt \
  -d "test_name=HbA1c Follow-up" \
  -d "result=5.8% - Normal range"
```

**Response:**

```
302 Found
Location: /doctor/appointments/123/
```

---

#### Add Prescription

**Endpoint:** `POST /doctor/add_prescription/<appointment_id>/`

**Authentication:** Required (Doctor)

Add medication prescription for patient.

**Path Parameters:**

| Parameter      | Type    | Description            |
| -------------- | ------- | ---------------------- |
| appointment_id | integer | Appointment identifier |

**Request Body:**

| Field       | Type | Required | Description                    |
| ----------- | ---- | -------- | ------------------------------ |
| medications | text | Yes      | List of prescribed medications |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/doctor/add_prescription/123/" \
  -b cookies.txt \
  -d "medications=1. Metformin 500mg - Twice daily after meals\n2. Aspirin 75mg - Once daily\n3. Atorvastatin 10mg - Once at night"
```

**Response:**

```
302 Found
Location: /doctor/appointments/123/
```

---

#### Edit Prescription

**Endpoint:** `POST /doctor/edit_prescription/<appointment_id>/<prescription_id>/`

**Authentication:** Required (Doctor)

Update existing prescription.

**Path Parameters:**

| Parameter       | Type    | Description             |
| --------------- | ------- | ----------------------- |
| appointment_id  | integer | Appointment identifier  |
| prescription_id | integer | Prescription identifier |

**Request Body:**

| Field       | Type | Required | Description             |
| ----------- | ---- | -------- | ----------------------- |
| medications | text | Yes      | Updated medication list |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/doctor/edit_prescription/123/89/" \
  -b cookies.txt \
  -d "medications=1. Metformin 850mg - Twice daily\n2. Aspirin 75mg - Once daily"
```

**Response:**

```
302 Found
Location: /doctor/appointments/123/
```

---

#### Doctor Payments

**Endpoint:** `GET /doctor/payments/`

**Authentication:** Required (Doctor)

View all completed appointments with payment information.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/doctor/payments/" \
  -b cookies.txt
```

**Response:** HTML page with payments list and total earnings

---

#### Doctor Notifications

**Endpoint:** `GET /doctor/notifications/`

**Authentication:** Required (Doctor)

Get unread notifications for the doctor.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/doctor/notifications/" \
  -b cookies.txt
```

**Response:** HTML page with notifications list

---

#### Doctor Profile

**Endpoint:** `GET, POST /doctor/profile/`

**Authentication:** Required (Doctor)

View and update doctor profile and availability.

**Request Body (POST):**

| Field                           | Type    | Required | Description            |
| ------------------------------- | ------- | -------- | ---------------------- |
| full_name                       | string  | Yes      | Full name              |
| mobile                          | string  | Yes      | Phone number           |
| country                         | string  | No       | Country                |
| bio                             | text    | No       | Professional biography |
| specialization                  | string  | Yes      | Medical specialization |
| qualifications                  | string  | Yes      | Medical qualifications |
| years_of_experience             | integer | Yes      | Years of practice      |
| next_available_appointment_date | date    | No       | Next available date    |
| image                           | file    | No       | Profile picture        |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/doctor/profile/" \
  -b cookies.txt \
  -F "full_name=Dr. Sarah Johnson" \
  -F "specialization=Cardiology" \
  -F "years_of_experience=12" \
  -F "image=@doctor_photo.jpg"
```

**Response:** Updated profile page with success message

---

## Error Handling

### Error Response Format

All errors return appropriate HTTP status codes with user-friendly messages in the response.

```html
<!-- HTML Error Page -->
<div class="error-message">
  <h2>Error: Invalid Request</h2>
  <p>The appointment slot is no longer available.</p>
</div>
```

### Common Error Scenarios

| Scenario            | Status Code | Description                             |
| ------------------- | ----------- | --------------------------------------- |
| Invalid credentials | 401         | Email or password incorrect             |
| Unauthorized access | 403         | User lacks permission for resource      |
| Resource not found  | 404         | Appointment, user, or service not found |
| Validation error    | 400         | Invalid input data                      |
| Slot unavailable    | 400         | Time slot already booked                |
| Session expired     | 401         | User needs to log in again              |
| Server error        | 500         | Internal server error occurred          |

---

## Status Codes

### HTTP Status Codes Used

| Code | Meaning               | Usage                                 |
| ---- | --------------------- | ------------------------------------- |
| 200  | OK                    | Successful GET request                |
| 302  | Found                 | Successful redirect after POST        |
| 400  | Bad Request           | Invalid input or business logic error |
| 401  | Unauthorized          | Authentication required or failed     |
| 403  | Forbidden             | Insufficient permissions              |
| 404  | Not Found             | Resource doesn't exist                |
| 500  | Internal Server Error | Server-side error                     |

### Appointment Status Values

| Status        | Description                                |
| ------------- | ------------------------------------------ |
| `pending`   | Appointment created, awaiting confirmation |
| `scheduled` | Confirmed with time slot                   |
| `completed` | Appointment finished                       |
| `cancelled` | Appointment cancelled by either party      |

---

## Changelog

### Version 1.0.0 (November 2025)

#### Added

- Complete authentication system (sign-up, sign-in, sign-out)
- Appointment booking and management
- Patient dashboard and medical history (E-Booklet)
- Doctor dashboard with appointment management
- Medical records management (diagnosis, treatment)
- Lab test ordering and results
- Prescription management
- Real-time notifications system
- AI chat assistant for medical queries
- Profile management for patients and doctors
- Slot-based scheduling system

#### Security

- Session-based authentication
- CSRF protection on all forms
- HttpOnly and Secure cookie flags
- Role-based access control
- Input validation and sanitization
