# MHMAS API Documentation

**Mobile Health Monitoring and Alert System**

Version: 1.0.0

---

## Overview

The MHMAS API provides a comprehensive backend system for managing patient health records, provider information, vital records, appointments, and health alerts. The API uses JWT (JSON Web Token) authentication for secure access.

## Base URL

- **Local Development**: `http://127.0.0.1:8000/api/`
- **Production**: `https://your-lambda-url.amazonaws.com/api/`

## Interactive Documentation

- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **OpenAPI Schema**: `/api/schema/`

---

## Authentication

### JWT Token Authentication

The API uses JWT tokens for authentication. Most endpoints require a valid access token in the request header.

**Header Format:**
```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### 1. Login (Obtain Token)

**Endpoint:** `POST /api/auth/login/`

**Description:** Authenticate a user and obtain JWT tokens.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

#### 2. Refresh Token

**Endpoint:** `POST /api/auth/refresh/`

**Description:** Obtain a new access token using a refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Registration Endpoints

### 1. Unified Registration

**Endpoint:** `POST /api/auth/register/`

**Description:** Register either a patient or provider based on the role field.

**Authentication:** Not required

**Request Body:**

**For Patient Registration:**
```json
{
  "role": "patient",
  "username": "john_doe",
  "password": "securepassword123",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "address": "123 Main St, City",
  "date_of_birth": "1990-01-15",
  "blood_group": "O+",
  "emergency_contact": "+0987654321"
}
```

**For Provider Registration:**
```json
{
  "role": "provider",
  "username": "dr_smith",
  "password": "securepassword123",
  "email": "dr.smith@hospital.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+1234567890",
  "specialization": "Cardiology",
  "license_number": "MED123456",
  "clinic_name": "City Heart Clinic"
}
```

**Response (201 Created):**
```json
{
  "message": "Patient registered successfully.",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "profile": {
    "id": 1,
    "user": {...},
    "phone": "+1234567890",
    "address": "123 Main St, City",
    ...
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

---

### 2. Patient Registration

**Endpoint:** `POST /api/auth/register/patient/`

**Description:** Register a new patient account.

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepassword123",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "address": "123 Main St, City",
  "date_of_birth": "1990-01-15",
  "blood_group": "O+",
  "emergency_contact": "+0987654321"
}
```

**Required Fields:**
- `username` (string)
- `password` (string)
- `first_name` (string)
- `last_name` (string)
- `phone` (string)
- `address` (string)
- `date_of_birth` (YYYY-MM-DD)

**Optional Fields:**
- `email` (string)
- `blood_group` (string)
- `emergency_contact` (string)

---

### 3. Provider Registration

**Endpoint:** `POST /api/auth/register/provider/`

**Description:** Register a new healthcare provider account.

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "dr_smith",
  "password": "securepassword123",
  "email": "dr.smith@hospital.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+1234567890",
  "specialization": "Cardiology",
  "license_number": "MED123456",
  "clinic_name": "City Heart Clinic"
}
```

**Required Fields:**
- `username` (string)
- `password` (string)
- `first_name` (string)
- `last_name` (string)
- `phone` (string)
- `specialization` (string)
- `license_number` (string)

**Optional Fields:**
- `email` (string)
- `clinic_name` (string)

---

## Patient Endpoints

### List Patients

**Endpoint:** `GET /api/patients/`

**Description:** Retrieve a list of patients. Patients see only their own data; providers see all patients.

**Authentication:** Required

**Query Parameters:**
- `page` (integer): Page number for pagination
- `search` (string): Search by username, email, first name, or last name

**Response (200 OK):**
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/patients/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
      },
      "phone": "+1234567890",
      "address": "123 Main St, City",
      "date_of_birth": "1990-01-15",
      "blood_group": "O+",
      "emergency_contact": "+0987654321",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

### Get Patient Details

**Endpoint:** `GET /api/patients/{id}/`

**Description:** Retrieve details of a specific patient.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "phone": "+1234567890",
  "address": "123 Main St, City",
  "date_of_birth": "1990-01-15",
  "blood_group": "O+",
  "emergency_contact": "+0987654321",
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

### Update Patient

**Endpoint:** `PUT /api/patients/{id}/` or `PATCH /api/patients/{id}/`

**Description:** Update patient information.

**Authentication:** Required

**Request Body (PATCH example):**
```json
{
  "phone": "+1111111111",
  "address": "456 New St, City"
}
```

---

### Delete Patient

**Endpoint:** `DELETE /api/patients/{id}/`

**Description:** Delete a patient record.

**Authentication:** Required

**Response (204 No Content)**

---

## Provider Endpoints

### List Providers

**Endpoint:** `GET /api/providers/`

**Description:** Retrieve a list of healthcare providers.

**Authentication:** Required

**Query Parameters:**
- `page` (integer): Page number
- `search` (string): Search by username, email, clinic name, or specialization

**Response (200 OK):**
```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "dr_smith",
        "email": "dr.smith@hospital.com"
      },
      "hospital_name": "City Hospital",
      "specialization": "Cardiology",
      "phone": "+1234567890",
      "address": "789 Medical Center Dr",
      "created_at": "2025-01-10T09:00:00Z"
    }
  ]
}
```

---

## Vital Records Endpoints

### List Vital Records

**Endpoint:** `GET /api/vitals/`

**Description:** Retrieve vital records. Patients see only their own; providers see all.

**Authentication:** Required

**Query Parameters:**
- `page` (integer)
- `search` (string): Search by patient name

**Response (200 OK):**
```json
{
  "count": 200,
  "results": [
    {
      "id": 1,
      "patient": {
        "id": 1,
        "user": {...}
      },
      "vital_type": "blood_pressure",
      "value": "120/80",
      "unit": "mmHg",
      "recorded_at": "2025-01-15T14:30:00Z",
      "notes": "Normal reading"
    }
  ]
}
```

---

### Create Vital Record

**Endpoint:** `POST /api/vitals/`

**Description:** Create a new vital record.

**Authentication:** Required

**Request Body:**
```json
{
  "patient": 1,
  "vital_type": "heart_rate",
  "value": "72",
  "unit": "bpm",
  "notes": "Resting heart rate"
}
```

---

## Appointment Endpoints

### List Appointments

**Endpoint:** `GET /api/appointments/`

**Description:** Retrieve appointments. Patients see their own; providers see appointments with them.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "patient": {...},
      "provider": {...},
      "date": "2025-01-20",
      "time": "10:00:00",
      "status": "scheduled",
      "reason": "Regular checkup",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

---

### Create Appointment

**Endpoint:** `POST /api/appointments/`

**Description:** Schedule a new appointment.

**Authentication:** Required

**Request Body:**
```json
{
  "patient": 1,
  "provider": 1,
  "date": "2025-01-20",
  "time": "10:00:00",
  "status": "scheduled",
  "reason": "Regular checkup"
}
```

---

## Alert Endpoints

### List Alerts

**Endpoint:** `GET /api/alerts/`

**Description:** Retrieve health alerts. Patients see their own; providers see all.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "patient": {...},
      "alert_type": "high_blood_pressure",
      "message": "Blood pressure reading is above normal range",
      "severity": "high",
      "created_at": "2025-01-15T15:00:00Z",
      "resolved": false
    }
  ]
}
```

---

### Create Alert

**Endpoint:** `POST /api/alerts/`

**Description:** Create a new health alert.

**Authentication:** Required

**Request Body:**
```json
{
  "patient": 1,
  "alert_type": "high_blood_pressure",
  "message": "Blood pressure reading is above normal range",
  "severity": "high"
}
```

---

### Update Alert (Mark as Resolved)

**Endpoint:** `PATCH /api/alerts/{id}/`

**Description:** Update an alert (e.g., mark as resolved).

**Authentication:** Required

**Request Body:**
```json
{
  "resolved": true
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing fields: username, password"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Common HTTP Status Codes

- **200 OK**: Request succeeded
- **201 Created**: Resource created successfully
- **204 No Content**: Request succeeded with no content to return
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

---

## Pagination

All list endpoints support pagination with the following parameters:

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `page_size` (integer): Number of items per page (default: 20)

**Response Format:**
```json
{
  "count": 100,
  "next": "http://example.com/api/resource/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Search and Filtering

Most list endpoints support searching through the `search` query parameter.

**Example:**
```
GET /api/patients/?search=john
```

---

## Best Practices

1. **Always use HTTPS** in production
2. **Store tokens securely** (never in localStorage for sensitive apps)
3. **Refresh tokens before expiry** to maintain sessions
4. **Handle errors gracefully** on the client side
5. **Validate data** before sending requests
6. **Use appropriate HTTP methods** (GET, POST, PUT, PATCH, DELETE)

---

## Testing with cURL

### Register a Patient
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/patient/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "address": "123 Main St",
    "date_of_birth": "1990-01-15",
    "email": "john@example.com"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### Get Patients (Authenticated)
```bash
curl -X GET http://127.0.0.1:8000/api/patients/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Support

For issues or questions:
- Visit Swagger UI at `/api/docs/` for interactive testing
- Check the OpenAPI schema at `/api/schema/`

---

**Last Updated:** January 2025
