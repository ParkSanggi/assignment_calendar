from django.db import models
from django.utils import timezone


class Schedule(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    is_all_day = models.BooleanField()


class Invitation(models.Model):
    name = models.CharField(max_length=30)
    e_mail = models.EmailField()
    is_accepted = models.BooleanField(default=False)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True, null=True, related_name='invitations')

