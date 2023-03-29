from django.contrib import admin
from .models import ViolationInfo, Violation


@admin.register(ViolationInfo)
class ViolationInfoAdmin(admin.ModelAdmin):
    """ViolationInfo class 관리"""

    list_display = (
        "name_list",
        "cctv",
    )

    def name_list(self, obj):
        # print("AAAAAAAAA", dir(obj.name))
        for i in obj.name.all():
            print(i.name)
        print()
        print()
        print()
        return ",".join([name.name for name in obj.name.all()])


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    """Violation class 관리"""

    list_display = ("name",)
