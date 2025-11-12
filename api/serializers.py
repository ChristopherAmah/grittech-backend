from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Provider, VitalRecord, Appointment, Alert


# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ----------------------------
# Provider Serializer
# ----------------------------
class ProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Provider
        fields = [
            'id', 'user', 'hospital_name', 'specialization',
            'phone', 'address', 'created_at'
        ]


# ----------------------------
# Patient Serializer
# ----------------------------
class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'provider', 'full_name', 'age',
            'weight', 'height', 'blood_type', 'medical_history',
            'created_at'
        ]


# ----------------------------
# Vital Record Serializer
# ----------------------------
class VitalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = VitalRecord
        fields = [
            'id', 'patient', 'vital_type', 'value', 'unit',
            'recorded_at', 'notes'
        ]


# ----------------------------
# Appointment Serializer
# ----------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'provider', 'date', 'time',
            'status', 'reason', 'created_at'
        ]


# ----------------------------
# Alert Serializer
# ----------------------------
class AlertSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id', 'patient', 'alert_type', 'message',
            'severity', 'created_at', 'resolved'
        ]


# ----------------------------
# Registration Serializers
# ----------------------------
class PatientRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    blood_group = serializers.CharField(required=False, allow_blank=True)
    emergency_contact = serializers.CharField(required=False, allow_blank=True)


class ProviderRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    specialization = serializers.CharField(required=True)
    license_number = serializers.CharField(required=True)
    clinic_name = serializers.CharField(required=False, allow_blank=True)


class UnifiedRegistrationSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['patient', 'provider'], required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    # Patient fields
    address = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    blood_group = serializers.CharField(required=False, allow_blank=True)
    emergency_contact = serializers.CharField(required=False, allow_blank=True)
    # Provider fields
    specialization = serializers.CharField(required=False, allow_blank=True)
    license_number = serializers.CharField(required=False, allow_blank=True)
    clinic_name = serializers.CharField(required=False, allow_blank=True)


class RegistrationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user = serializers.DictField()
    profile = serializers.DictField()
    tokens = serializers.DictField()
