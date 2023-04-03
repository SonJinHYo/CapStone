from django.urls import path
from . import views

urlpatterns = [
    path("service", views.AllViolations.as_view(), name="all_violations"),
    path("choice", views.Choice.as_view(), name="choice"),
]
