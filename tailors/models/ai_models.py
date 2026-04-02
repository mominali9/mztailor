from django.db import models
from django.contrib.auth.models import User

class MeasurementProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='measurements')
    height_cm = models.FloatField(help_text="User provided height in cm")
    chest_cm = models.FloatField()
    waist_cm = models.FloatField()
    shoulder_cm = models.FloatField()
    arm_length_cm = models.FloatField()
    recommended_size = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
