from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from hospital.models import HospitalProfile


class EmergencyRequest(models.Model):

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    hospital = models.ForeignKey(
        HospitalProfile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    reason = models.TextField()
    location = models.CharField(max_length=255)

    latitude = models.FloatField()
    longitude = models.FloatField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    ai_analysis = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.priority} - {self.status}"