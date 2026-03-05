from django.db import models
from users.models import User


# Hospital Specialities
SPECIALITY_CHOICES = (
    ("cardiology", "Cardiology"),
    ("trauma", "Trauma"),
    ("orthopedic", "Orthopedic"),
    ("neurology", "Neurology"),
    ("pediatric", "Pediatric"),
    ("general", "General Emergency"),
)


class HospitalProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    hospital_name = models.CharField(max_length=200)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    city = models.CharField(max_length=255, null=True, blank=True)

    license_number = models.CharField(max_length=100)

    # 🔥 NEW FIELD (hospital treatments)
    specialities = models.JSONField(blank=True, null=True)

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return self.hospital_name