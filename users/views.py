from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.conf import settings
from .models import User
from hospital.models import HospitalProfile
from doctors.models import DoctorProfile
from django.shortcuts import get_object_or_404
from records.models import TreatmentRecord, MedicalActionLog
import random
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from records.models import TreatmentRecord
from .services.health_ai import generate_health_summary
from .services.site_ai import site_assistant
import threading





# ---------------- HOME (Landing Page) ----------------

def home(request):
    from hospital.models import HospitalProfile
    hospitals = HospitalProfile.objects.filter(status="approved")[:3]
    return render(request, "home.html", {"hospitals": hospitals})





def all_hospitals(request):

    hospitals = HospitalProfile.objects.filter(status="approved")

    return render(request, "all_hospitals.html", {
        "hospitals": hospitals
    })

# ---------------- CITIZEN REGISTER ----------------

def citizen_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return render(request, "citizen_register.html", {"error": "Email already exists"})

        user = User.objects.create_user(
            email=email,
            name=name,
            password=password,
            role="citizen"
        )

        login(request, user)
        return redirect("citizen_profile")

    return render(request, "citizen_register.html")


# ---------------- CITIZEN LOGIN ----------------

def citizen_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user and user.role == "citizen":
            login(request, user)
            return redirect("citizen_profile")

        return render(request, "citizen_login.html", {"error": "Invalid Credentials"})

    return render(request, "citizen_login.html")


# ---------------- CITIZEN DASHBOARD ----------------


@login_required
def citizen_profile(request):

    if request.user.role != "citizen":
        return redirect("home")

    records = TreatmentRecord.objects.filter(
        patient=request.user
    ).order_by("-created_at")

    ai_summary = None

    # 👇 Button click hone par AI run hoga
    if request.method == "POST":

        history_text = ""

        if records.exists():
            for r in records:
                history_text += f"""
Disease: {r.disease}
Medication: {r.medication}
Date: {r.created_at}
---
"""
        else:
            history_text = "No medical records available."

        ai_summary = generate_health_summary(history_text)

    return render(request, "citizen_profile.html", {
        "user": request.user,
        "records": records,
        "ai_summary": ai_summary
    })

# ---------------- LOGOUT ----------------

@login_required
def citizen_logout(request):
    logout(request)
    return redirect("home")





def hospital_detail(request, hospital_id):

    hospital = HospitalProfile.objects.get(id=hospital_id)

    doctors = DoctorProfile.objects.filter(
        hospital=hospital,
        hospital_status="approved",
        status="approved"
    )

    return render(request, "hospital_detail.html", {
        "hospital": hospital,
        "doctors": doctors
    })


def doctor_public_profile(request, doctor_id):

    doctor = get_object_or_404(
        DoctorProfile,
        id=doctor_id,
        hospital_status="approved",
        status="approved"
    )

    return render(request, "doctor_public_profile.html", {
        "doctor": doctor
    })



def access_by_health_id(request):

    if request.method == "POST":

        health_id = request.POST.get("health_id")

        return redirect("access_by_qr", health_id=health_id)

    return redirect("home")











# def access_by_qr(request, health_id):

#     user = get_object_or_404(User, unique_health_id=health_id, role="citizen")

#     otp = str(random.randint(100000, 999999))

#     request.session["qr_otp"] = otp
#     request.session["qr_user_id"] = user.id

#     send_mail(
#         "PulseID Access OTP",
#         f"Your OTP is {otp}",
#         "noreply@pulseid.com",
#         [user.email],
#         fail_silently=True,
#     )

#     return render(request, "qr_verify.html", {"health_id": health_id})






# 🔥 async email sender
def send_otp_email(email, otp):
    try:
        send_mail(
            subject="PulseID Access OTP",
            message=f"Your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        print("EMAIL ERROR:", e)


def access_by_qr(request, health_id):

    user = get_object_or_404(User, unique_health_id=health_id, role="citizen")

    otp = str(random.randint(100000, 999999))

    # 🔐 session store
    request.session["qr_otp"] = otp
    request.session["qr_user_id"] = user.id

    # 🚀 background email
    thread = threading.Thread(target=send_otp_email, args=(user.email, otp))
    thread.daemon = True
    thread.start()

    return render(request, "qr_verify.html", {"health_id": health_id})





def verify_qr_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        if entered_otp == request.session.get("qr_otp"):

            user_id = request.session.get("qr_user_id")
            return redirect("qr_profile_view", user_id=user_id)

        return render(request, "qr_verify.html", {"error": "Invalid OTP"})

    return redirect("home")




def qr_profile_view(request, user_id):

    user = User.objects.get(id=user_id)

    records = TreatmentRecord.objects.filter(patient=user)

    return render(request, "qr_profile.html", {
        "user": user,
        "records": records
    })





def ai_chat(request):

    response = None

    if request.method == "POST":

        question = request.POST.get("question")

        print("USER QUESTION:", question)

        response = site_assistant(question)

        print("AI RESPONSE:", response)

    return render(request, "ai_chat.html", {
        "response": response
    })




def ai_chat_api(request):

    if request.method == "POST":

        question = request.POST.get("message")

        answer = site_assistant(question)

        return JsonResponse({
            "reply": answer
        })