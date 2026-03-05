from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from doctors.models import DoctorProfile
from users.models import User
from .models import HospitalProfile
from emergency.models import EmergencyRequest


def hospital_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        hospital_name = request.POST.get("hospital_name")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        city = request.POST.get("city")
        license_number = request.POST.get("license_number")
        specialities = request.POST.getlist("specialities")

        if User.objects.filter(email=email).exists():
            return render(request, "hospital_register.html", {"error": "Email already exists"})

        user = User.objects.create_user(
            email=email,
            name=name,
            password=password,
            role="hospital"
        )

        HospitalProfile.objects.create(
            user=user,
            hospital_name=hospital_name,
            latitude=latitude,
            longitude=longitude,
            city=city,
            license_number=license_number,
            specialities=specialities

        )

        login(request, user)
        return redirect("hospital_dashboard")

    return render(request, "hospital_register.html")


def hospital_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user and user.role == "hospital":
            login(request, user)
            return redirect("hospital_dashboard")

        return render(request, "hospital_login.html", {"error": "Invalid Credentials"})

    return render(request, "hospital_login.html")



@login_required
def approve_doctor_by_hospital(request, doctor_id):

    doctor = DoctorProfile.objects.get(id=doctor_id)

    if request.user.role != "hospital":
        return redirect("home")

    doctor.hospital_status = "approved"
    doctor.save()

    return redirect("hospital_dashboard")


@login_required
def hospital_dashboard(request):

    if request.user.role != "hospital":
        return redirect("home")

    profile = HospitalProfile.objects.get(user=request.user)

    # 🔹 Doctor Requests
    pending_doctors = DoctorProfile.objects.filter(
        hospital=profile,
        status="pending"
    )

    approved_doctors = DoctorProfile.objects.filter(
        hospital=profile,
        status="approved"
    )

    # 🔥 Emergency Requests (NEW)
    emergency_requests = EmergencyRequest.objects.filter(
        hospital=profile
    ).order_by("-created_at")

    emergency_requests = EmergencyRequest.objects.filter(
        hospital=profile
    ).exclude(status="completed")

    context = {
        "profile": profile,
        "pending_doctors": pending_doctors,
        "approved_doctors": approved_doctors,
        "emergency_requests": emergency_requests
    }

    return render(request, "hospital_dashboard.html", context)