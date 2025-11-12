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
