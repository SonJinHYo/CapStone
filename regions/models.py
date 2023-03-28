from django.db import models


class Region(models.Model):
    """Description Region Class"""

    region_name = models.CharField(max_length=50)
    violation_count = models.PositiveIntegerField()
