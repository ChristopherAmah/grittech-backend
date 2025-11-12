# from django.shortcuts import render


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.db import connections
# from django.db.utils import OperationalError

# @api_view(["GET"])
# def health_check(request):
#     """Simple API health check endpoint"""
#     db_status = "up"
#     try:
#         db_conn = connections['default']
#         db_conn.cursor()
#     except OperationalError:
#         db_status = "down"

#     data = {
#         "status": "ok" if db_status == "up" else "error",
#         "database": db_status,
#         "message": "Service is healthy" if db_status == "up" else "Database connection failed"
#     }

#     return Response(data, status=status.HTTP_200_OK if db_status == "up" else status.HTTP_503_SERVICE_UNAVAILABLE)

from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, filters, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Patient, Provider, VitalRecord, Appointment, Alert
from .serializers import (
    PatientSerializer, ProviderSerializer, VitalRecordSerializer,
    AppointmentSerializer, AlertSerializer, PatientRegistrationSerializer,
    ProviderRegistrationSerializer, UnifiedRegistrationSerializer,
    RegistrationResponseSerializer
)

User = get_user_model()


# ----------------------------
# Patient ViewSet
# ----------------------------
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'provider_profile'):
            return Patient.objects.all()
        return Patient.objects.filter(user=user)


# ----------------------------
# Provider ViewSet
# ----------------------------
class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__email', 'clinic_name', 'specialization']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'provider_profile'):
            return Provider.objects.filter(user=user)
        return Provider.objects.none()


# ----------------------------
# VitalRecord ViewSet
# ----------------------------
class VitalRecordViewSet(viewsets.ModelViewSet):
    queryset = VitalRecord.objects.all()
    serializer_class = VitalRecordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__user__first_name', 'patient__user__last_name']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'provider_profile'):
            return VitalRecord.objects.all()
        return VitalRecord.objects.filter(patient__user=user)


# ----------------------------
# Appointment ViewSet
# ----------------------------
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__user__first_name', 'provider__user__last_name', 'status']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'provider_profile'):
            return Appointment.objects.filter(provider__user=user)
        return Appointment.objects.filter(patient__user=user)


# ----------------------------
# Alert ViewSet
# ----------------------------
class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__user__first_name', 'message']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'provider_profile'):
            return Alert.objects.all()
        return Alert.objects.filter(patient__user=user)


# ----------------------------
# Custom Registration Endpoints (Class-Based Views)
# ----------------------------
class PatientRegistrationView(generics.CreateAPIView):
    """Register a new patient and linked user account."""
    serializer_class = PatientRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ['username', 'password', 'first_name', 'last_name', 'phone', 'address', 'date_of_birth']
        missing = [f for f in required_fields if f not in data]

        if missing:
            return Response({"error": f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=data['username']).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email', ''),
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        patient = Patient.objects.create(
            user=user,
            phone=data['phone'],
            address=data['address'],
            date_of_birth=data['date_of_birth'],
            blood_group=data.get('blood_group'),
            emergency_contact=data.get('emergency_contact'),
        )

        serializer = PatientSerializer(patient)
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Patient registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "profile": serializer.data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)


class ProviderRegistrationView(generics.CreateAPIView):
    """Register a new healthcare provider and linked user account."""
    serializer_class = ProviderRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ['username', 'password', 'first_name', 'last_name', 'phone', 'specialization', 'license_number']
        missing = [f for f in required_fields if f not in data]

        if missing:
            return Response({"error": f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=data['username']).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email', ''),
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        provider = Provider.objects.create(
            user=user,
            phone=data['phone'],
            specialization=data['specialization'],
            license_number=data['license_number'],
            clinic_name=data.get('clinic_name')
        )

        serializer = ProviderSerializer(provider)
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Provider registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "profile": serializer.data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)


class UnifiedRegistrationView(generics.CreateAPIView):
    """
    Unified registration endpoint for both Patients and Providers.
    Expected fields:
    role: "patient" or "provider"
    username, password, email, first_name, last_name, phone, ...
    """
    serializer_class = UnifiedRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        role = request.data.get('role')
        if not role or role not in ['patient', 'provider']:
            return Response({"error": "Missing or invalid 'role'. Must be 'patient' or 'provider'."}, status=400)

        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=request.data.get('email', ''),
            first_name=request.data.get('first_name', ''),
            last_name=request.data.get('last_name', '')
        )

        # Create role profile
        if role == 'patient':
            patient = Patient.objects.create(
                user=user,
                phone=request.data.get('phone'),
                address=request.data.get('address'),
                date_of_birth=request.data.get('date_of_birth'),
                blood_group=request.data.get('blood_group'),
                emergency_contact=request.data.get('emergency_contact'),
            )
            profile_serializer = PatientSerializer(patient)
        else:
            provider = Provider.objects.create(
                user=user,
                phone=request.data.get('phone'),
                specialization=request.data.get('specialization'),
                license_number=request.data.get('license_number'),
                clinic_name=request.data.get('clinic_name'),
            )
            profile_serializer = ProviderSerializer(provider)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": f"{role.capitalize()} registered successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "profile": profile_serializer.data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=201)
