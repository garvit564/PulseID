from django.db import models
from users.models import User
from doctors.models import DoctorProfile
from hospital.models import HospitalProfile


class TreatmentRecord(models.Model):

    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalProfile, on_delete=models.CASCADE)

    disease = models.CharField(max_length=255)
    medication = models.TextField()
    report_image = models.ImageField(upload_to="medical_reports/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.disease}"


class MedicalActionLog(models.Model):

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    action = models.CharField(max_length=100)  # Add/Edit/Delete
    description = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.doctor.user.name}"