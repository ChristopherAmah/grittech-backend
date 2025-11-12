from django.contrib import admin
from .models import Provider, Patient, VitalRecord, Appointment, Alert


# ----------------------------
# Provider Admin
# ----------------------------
@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital_name', 'specialization', 'phone', 'created_at')
    search_fields = ('user__username', 'hospital_name', 'specialization', 'phone')
    list_filter = ('specialization', 'created_at')


# ----------------------------
# Patient Admin
# ----------------------------
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'provider', 'age', 'weight', 'height', 'blood_type', 'created_at')
    search_fields = ('full_name', 'user__username', 'provider__hospital_name', 'blood_type')
    list_filter = ('blood_type', 'provider', 'created_at')


# ----------------------------
# VitalRecord Admin
# ----------------------------
@admin.register(VitalRecord)
class VitalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'vital_type', 'value', 'unit', 'recorded_at')
    search_fields = ('patient__full_name', 'vital_type')
    list_filter = ('vital_type', 'recorded_at')


# ----------------------------
# Appointment Admin
# ----------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'date', 'time', 'status', 'reason', 'created_at')
    search_fields = ('patient__full_name', 'provider__user__username', 'status')
    list_filter = ('status', 'date', 'provider')


# ----------------------------
# Alert Admin
# ----------------------------
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('patient', 'alert_type', 'severity', 'resolved', 'created_at')
    search_fields = ('patient__full_name', 'alert_type', 'message')
    list_filter = ('severity', 'resolved', 'created_at')
