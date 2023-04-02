from django.contrib import admin
from .models import CCTV, Video


@admin.register(CCTV)
class CCTVAdmin(admin.ModelAdmin):
    """CCTV class를 관리"""

    list_display = (
        "name",
        "region",
        "description",
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Video class를 관리"""
