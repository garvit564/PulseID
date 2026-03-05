from django.shortcuts import render, redirect, get_object_or_404
from users.models import User
from hospital.models import HospitalProfile
from .models import EmergencyRequest
from .services.ai_service import analyze_emergency
from records.models import TreatmentRecord
from django.contrib.auth.decorators import login_required
import math


def emergency_form(request):

    if request.method == "POST":

        health_id = request.POST.get("health_id")
        reason = request.POST.get("reason")
        location = request.POST.get("location")

        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")

        if not lat or not lon:
            return render(request, "emergency_form.html", {
                "error": "Please select location from suggestions."
            })

        latitude = float(lat)
        longitude = float(lon)

        try:
            patient = User.objects.get(
                unique_health_id=health_id,
                role="citizen"
            )
        except User.DoesNotExist:
            return render(request, "emergency_form.html", {
                "error": "Invalid Health ID"
            })

        # 🔥 Fetch Treatment History
        records = TreatmentRecord.objects.filter(patient=patient)

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
            history_text = "No prior medical records available."

        # 🤖 AI Analysis
        priority, speciality, explanation = analyze_emergency(history_text, reason)

        hospitals = HospitalProfile.objects.filter(status="approved")

        # 🔍 First find hospitals with matching speciality
        matching_hospitals = []

        for h in hospitals:
            if h.specialities and speciality in h.specialities:
                matching_hospitals.append(h)

        # If no speciality hospital found → fallback to all hospitals
        search_pool = matching_hospitals if matching_hospitals else hospitals

        nearest = None
        min_distance = float("inf")

        for h in search_pool:

            if h.latitude and h.longitude:

                distance = math.sqrt(
                    (h.latitude - latitude) ** 2 +
                    (h.longitude - longitude) ** 2
                )

                if distance < min_distance:
                    min_distance = distance
                    nearest = h

        emergency = EmergencyRequest.objects.create(
            patient=patient,
            hospital=nearest,
            reason=reason,
            location=location,
            latitude=latitude,
            longitude=longitude,
            priority=priority,
            required_speciality=speciality,
            ai_analysis=explanation,
            status="pending",
        )

        return redirect("emergency_status", emergency_id=emergency.id)

    return render(request, "emergency_form.html")




@login_required
def ambulance_runout(request, emergency_id):

    emergency = get_object_or_404(EmergencyRequest, id=emergency_id)

    if request.user.role != "hospital":
        return redirect("home")

    current_hospital = emergency.hospital
    speciality = emergency.required_speciality

    hospitals = HospitalProfile.objects.filter(
        status="approved"
    ).exclude(id=current_hospital.id)

    matching = []

    for h in hospitals:

        if h.specialities and speciality in h.specialities:
            matching.append(h)

    search_pool = matching if matching else hospitals

    nearest = None
    min_distance = float("inf")

    for h in search_pool:

        if h.latitude and h.longitude:

            distance = math.sqrt(
                (h.latitude - emergency.latitude) ** 2 +
                (h.longitude - emergency.longitude) ** 2
            )

            if distance < min_distance:
                min_distance = distance
                nearest = h

    if nearest:

        emergency.previous_hospital = current_hospital
        emergency.hospital = nearest
        emergency.rerouted = True

        # 🔥 RESET STATUS PROPERLY
        emergency.status = "pending"

        emergency.save()

    return redirect("hospital_dashboard")




@login_required
def start_emergency(request, emergency_id):

    emergency = get_object_or_404(EmergencyRequest, id=emergency_id)

    if request.user.role != "hospital":
        return redirect("home")

    emergency.status = "in_progress"
    emergency.save()

    return redirect("hospital_dashboard")


@login_required
def mark_emergency_completed(request, emergency_id):

    emergency = get_object_or_404(EmergencyRequest, id=emergency_id)

    if request.user.role != "hospital":
        return redirect("home")

    emergency.status = "completed"
    emergency.save()

    return redirect("hospital_dashboard")


def emergency_status(request, emergency_id):

    emergency = get_object_or_404(EmergencyRequest, id=emergency_id)

    return render(request, "emergency_status.html", {
        "emergency": emergency
    })