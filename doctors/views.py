from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from users.models import User
from hospital.models import HospitalProfile
from .models import DoctorProfile
import random
from django.core.mail import send_mail
from records.models import TreatmentRecord, MedicalActionLog
from users.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def doctor_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        specialization = request.POST.get("specialization")
        license_number = request.POST.get("license_number")
        hospital_id = request.POST.get("hospital")

        if User.objects.filter(email=email).exists():
            return render(request, "doctor_register.html", {
                "error": "Email already exists",
                "hospitals": HospitalProfile.objects.filter(status="approved")
            })

        try:
            hospital = HospitalProfile.objects.get(
                id=hospital_id,
                status="approved"
            )
        except HospitalProfile.DoesNotExist:
            return redirect("doctor_register")

        user = User.objects.create_user(
            email=email,
            name=name,
            password=password,
            role="doctor"
        )

        DoctorProfile.objects.create(
            user=user,
            hospital=hospital,
            specialization=specialization,
            license_number=license_number
        )

        return redirect("doctor_login")

    hospitals = HospitalProfile.objects.filter(status="approved")

    return render(request, "doctor_register.html", {
        "hospitals": hospitals
    })





def doctor_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user and user.role == "doctor":
            login(request, user)
            return redirect("doctor_dashboard")

        return render(request, "doctor_login.html", {"error": "Invalid credentials"})

    return render(request, "doctor_login.html")





from django.contrib.auth.decorators import login_required

@login_required
def doctor_dashboard(request):

    if request.user.role != "doctor":
        return redirect("home")

    profile = DoctorProfile.objects.get(user=request.user)

    return render(request, "doctor_dashboard.html", {"profile": profile})








@login_required
def access_patient(request):

    if request.user.role != "doctor":
        return redirect("home")

    if request.method == "POST":

        health_id = request.POST.get("health_id")

        try:
            patient = User.objects.get(unique_health_id=health_id, role="citizen")
        except User.DoesNotExist:
            return render(request, "access_patient.html", {"error": "Patient not found"})

        otp = str(random.randint(100000, 999999))

        request.session['otp'] = otp
        request.session['patient_id'] = patient.id

        send_mail(
            "PulseID Access OTP",
            f"Your OTP is {otp}",
            "noreply@pulseid.com",
            [patient.email],
            fail_silently=True,
        )

        return render(request, "verify_otp.html", {
            "debug_otp": otp   # 👈 screen pe show karne ke liye
        })

    return render(request, "access_patient.html")





@login_required
def verify_patient_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        if entered_otp == request.session.get("otp"):

            patient_id = request.session.get("patient_id")
            return redirect("doctor_patient_card", patient_id)

        return render(request, "verify_otp.html", {"error": "Invalid OTP"})

    return redirect("doctor_dashboard")



@login_required
def doctor_patient_card(request, patient_id):

    if request.user.role != "doctor":
        return redirect("home")

    doctor_profile = DoctorProfile.objects.get(user=request.user)
    patient = User.objects.get(id=patient_id)

    records = TreatmentRecord.objects.filter(patient=patient)

    return render(request, "patient_card.html", {
        "patient": patient,
        "records": records
    })




@login_required
def add_record(request, patient_id):

    doctor_profile = DoctorProfile.objects.get(user=request.user)
    patient = User.objects.get(id=patient_id)

    if request.method == "POST":

        disease = request.POST.get("disease")
        medication = request.POST.get("medication")
        report_image = request.FILES.get("report_image")

        TreatmentRecord.objects.create(
            patient=patient,
            doctor=doctor_profile,
            hospital=doctor_profile.hospital,
            disease=disease,
            medication=medication,
            report_image=report_image
        )

        MedicalActionLog.objects.create(
            doctor=doctor_profile,
            patient=patient,
            action="Add",
            description=f"Added disease {disease}"
        )

        return redirect("doctor_patient_card", patient.id)

    return redirect("doctor_patient_card", patient.id)



@login_required
def delete_record(request, record_id):

    record = TreatmentRecord.objects.get(id=record_id)
    doctor_profile = DoctorProfile.objects.get(user=request.user)

    MedicalActionLog.objects.create(
        doctor=doctor_profile,
        patient=record.patient,
        action="Delete",
        description=f"Deleted disease {record.disease}"
    )

    patient_id = record.patient.id
    record.delete()

    return redirect("doctor_patient_card", patient_id)