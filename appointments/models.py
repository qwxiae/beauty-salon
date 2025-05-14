from django.db import models
from main.models import Procedure, Specialist
from django.conf import settings


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Appointment {self.id} from {self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'


class AppointmentItem(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='items',
                              on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f'{self.quantity} x {self.procedure} ({self.specialist})'
    

    class Meta:
        verbose_name = 'Appointment Item'
        verbose_name_plural = 'Appointment Items'
        