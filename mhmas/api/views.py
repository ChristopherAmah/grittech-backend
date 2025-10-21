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



from rest_framework import viewsets
from .models import Patient, Provider, VitalRecord, Appointment, Alert
from .serializers import (
    PatientSerializer, ProviderSerializer, VitalRecordSerializer,
    AppointmentSerializer, AlertSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class VitalRecordViewSet(viewsets.ModelViewSet):
    queryset = VitalRecord.objects.all()
    serializer_class = VitalRecordSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
