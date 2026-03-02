from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from hospital.models import HospitalProfile
from doctors.models import DoctorProfile

# ---------------- GOVT LOGIN ----------------

def govt_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user and user.role == "govt":
            login(request, user)
            return redirect("govt_dashboard")

        return render(request, "govt_login.html", {"error": "Invalid Credentials"})

    return render(request, "govt_login.html")


# ---------------- GOVT DASHBOARD ----------------

@login_required
def govt_dashboard(request):

    if request.user.role != "govt":
        return redirect("govt_login")

    pending_hospitals = HospitalProfile.objects.filter(status="pending")
    approved_hospitals = HospitalProfile.objects.filter(status="approved")
    rejected_hospitals = HospitalProfile.objects.filter(status="rejected")

    pending_doctors = DoctorProfile.objects.filter(
    hospital_status="approved",
    status="pending"
)
    approved_doctors = DoctorProfile.objects.filter(status="approved")
    rejected_doctors = DoctorProfile.objects.filter(status="rejected")

    context = {
        "pending_hospitals": pending_hospitals,
        "approved_hospitals": approved_hospitals,
        "rejected_hospitals": rejected_hospitals,
        "pending_doctors": pending_doctors,
        "approved_doctors": approved_doctors,
        "rejected_doctors": rejected_doctors,
    }

    return render(request, "govt_dashboard.html", context)


# ---------------- APPROVE ----------------

@login_required
def approve_hospital(request, hospital_id):

    if request.user.role != "govt":
        return redirect("govt_login")

    hospital = get_object_or_404(HospitalProfile, id=hospital_id)

    hospital.status = "approved"
    hospital.save()

    return redirect("govt_dashboard")


# ---------------- REJECT ----------------

@login_required
def reject_hospital(request, hospital_id):

    if request.user.role != "govt":
        return redirect("govt_login")

    hospital = get_object_or_404(HospitalProfile, id=hospital_id)

    hospital.status = "rejected"
    hospital.save()

    return redirect("govt_dashboard")



@login_required
def approve_doctor(request, doctor_id):

    if request.user.role != "govt":
        return redirect("govt_login")

    doctor = DoctorProfile.objects.get(id=doctor_id)
    doctor.status = "approved"
    doctor.save()

    return redirect("govt_dashboard")


@login_required
def reject_doctor(request, doctor_id):

    if request.user.role != "govt":
        return redirect("govt_login")

    doctor = DoctorProfile.objects.get(id=doctor_id)
    doctor.status = "rejected"
    doctor.save()

    return redirect("govt_dashboard")