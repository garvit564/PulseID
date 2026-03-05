from django.urls import path
from . import views

urlpatterns = [
    path("", views.emergency_form, name="emergency_form"),
    path("start/<int:emergency_id>/", views.start_emergency, name="start_emergency"),
    path("status/<int:emergency_id>/", views.emergency_status, name="emergency_status"),
    path("complete/<int:emergency_id>/", views.mark_emergency_completed, name="complete_emergency"),
    path(
    "runout/<int:emergency_id>/",
    views.ambulance_runout,
    name="ambulance_runout"
),
]