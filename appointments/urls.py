from django.urls import path
from .views import appointment_create, appointment_success, appointment_failure


app_name = 'appointments'

urlpatterns = [
    path('create/', appointment_create, name='appointment_create'),
    path('completed/', appointment_success, name='appointment_success'),
    path('failure/', appointment_failure, name='appointment_failure'),
]
