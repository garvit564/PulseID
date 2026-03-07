from django.shortcuts import render

# Create your views here.
import requests
import base64
from django.conf import settings


from django.shortcuts import render, redirect
from .models import TreatmentRecord
from .services.report_ai import analyze_report


def analyze_report_view(request, record_id):

    record = TreatmentRecord.objects.get(id=record_id)

    if not record.report_image:
        return redirect("citizen_profile")

    analysis = analyze_report(record.report_image.path)

    return render(request, "report_analysis.html", {
        "record": record,
        "analysis": analysis
    })