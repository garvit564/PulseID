from django.db import models
from users.models import User
from hospital.models import HospitalProfile


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalProfile, on_delete=models.CASCADE)

    specialization = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100)

    # 🏥 Hospital Level Approval
    HOSPITAL_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    hospital_status = models.CharField(
        max_length=20,
        choices=HOSPITAL_STATUS_CHOICES,
        default="pending"
    )

    # 🏛 Government Level Approval
    GOVT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    status = models.CharField(
        max_length=20,
        choices=GOVT_STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return self.user.name