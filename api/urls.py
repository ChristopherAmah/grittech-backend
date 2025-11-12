# core/urls.py
# from django.urls import path
# from .views import health_check

# urlpatterns = [
#     path("health/", health_check, name="health_check"),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    PatientViewSet,
    ProviderViewSet,
    VitalRecordViewSet,
    AppointmentViewSet,
    AlertViewSet,
    PatientRegistrationView,
    ProviderRegistrationView,
    UnifiedRegistrationView,
)

# Router for main model endpoints
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'providers', ProviderViewSet, basename='providers')
router.register(r'vitals', VitalRecordViewSet, basename='vitals')
router.register(r'appointments', AppointmentViewSet, basename='appointments')
router.register(r'alerts', AlertViewSet, basename='alerts')

# Main API routes
urlpatterns = [
    # Model endpoints
    path('', include(router.urls)),

    # Authentication routes
    path('auth/register/', UnifiedRegistrationView.as_view(), name='custom_register'),
    path('auth/register/patient/', PatientRegistrationView.as_view(), name='register_patient'),
    path('auth/register/provider/', ProviderRegistrationView.as_view(), name='register_provider'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
