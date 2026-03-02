from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.doctor_register, name="doctor_register"),
    path("login/", views.doctor_login, name="doctor_login"),
    path("dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("access-patient/", views.access_patient, name="access_patient"),
    path("verify-otp/", views.verify_patient_otp, name="verify_patient_otp"),
    path("patient/<int:patient_id>/", views.doctor_patient_card, name="doctor_patient_card"),
    path("add-record/<int:patient_id>/", views.add_record, name="add_record"),
    path("delete-record/<int:record_id>/", views.delete_record, name="delete_record"),
]