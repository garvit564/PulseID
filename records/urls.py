from django.urls import path
from . import views

urlpatterns = [
path("analyze-report/<int:record_id>/", views.analyze_report_view, name="analyze_report")
]