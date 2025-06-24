from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    c_type = models.CharField(max_length=10)  # ПТО/ССО
    group = models.CharField(max_length=100, null=True, blank=True)
    prev = models.TextField(blank=True)
    desc = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.title}"