from django.urls import path
from . import views

urlpatterns = [
    path("service", views.AllViolations.as_view(), name="all_violations"),
    path("choice/<str:kind>", views.Choice.as_view(), name="choice"),
    path(
        "service/<str:choice1>/<str:choice2>",
        views.ViolationDetail.as_view(),
        name="violation_detail",
    ),
]
