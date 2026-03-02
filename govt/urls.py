from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.govt_login, name="govt_login"),
    path("dashboard/", views.govt_dashboard, name="govt_dashboard"),

    path("approve/<int:hospital_id>/", views.approve_hospital, name="approve_hospital"),
    path("reject/<int:hospital_id>/", views.reject_hospital, name="reject_hospital"),
    path("approve-doctor/<int:doctor_id>/", views.approve_doctor, name="approve_doctor"),
    path("reject-doctor/<int:doctor_id>/", views.reject_doctor, name="reject_doctor"),
]