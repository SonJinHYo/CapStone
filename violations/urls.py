from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllViolations.as_view(), name="all_violations"),
    path("choice/<str:kind>", views.Choice.as_view(), name="choice"),
    path(
        "choice/<str:kind>/<str:detail>",
        views.ViolationDetail.as_view(),
        name="violation_detail",
    ),
]
