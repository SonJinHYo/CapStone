from django.urls import path
from . import views

urlpatterns = [
    path("service", views.AllViolations.as_view()),
]
