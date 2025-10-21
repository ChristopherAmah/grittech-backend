# core/urls.py
# from django.urls import path
# from .views import health_check

# urlpatterns = [
#     path("health/", health_check, name="health_check"),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, ProviderViewSet, VitalRecordViewSet,
    AppointmentViewSet, AlertViewSet
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'providers', ProviderViewSet)
router.register(r'vitals', VitalRecordViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
