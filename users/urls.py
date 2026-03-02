from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.citizen_register, name="citizen_register"),
    path("login/", views.citizen_login, name="citizen_login"),
    path("profile/", views.citizen_profile, name="citizen_profile"),
    path("logout/", views.citizen_logout, name="citizen_logout"),
    path("hospital/<int:hospital_id>/", views.hospital_detail, name="hospital_detail"),
    path("doctor/<int:doctor_id>/", views.doctor_public_profile, name="doctor_public_profile"),
    path("access-id/", views.access_by_health_id, name="access_by_health_id"),
    path("access/<str:health_id>/", views.access_by_qr, name="access_by_qr"),
    path("verify-otp/", views.verify_qr_otp, name="verify_qr_otp"),
    path("qr-profile/<int:user_id>/", views.qr_profile_view, name="qr_profile_view"),
]