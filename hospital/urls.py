from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.hospital_register, name="hospital_register"),
    path("login/", views.hospital_login, name="hospital_login"),
    path("dashboard/", views.hospital_dashboard, name="hospital_dashboard"),
    path("approve-doctor/<int:doctor_id>/",
     views.approve_doctor_by_hospital,
     name="approve_doctor_by_hospital"),
]