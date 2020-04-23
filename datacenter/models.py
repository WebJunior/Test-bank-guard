from django.db import models
from django.utils import timezone
import datetime

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)


    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
      if self.leaved_at is None:
        return timezone.now() - self.entered_at
      
      leaved_date = timezone.localtime(self.leaved_at)
      return leaved_date - self.entered_at


    def format_duration(self, duration):
      seconds = round(duration.total_seconds())
      hours =  seconds // 3600
      minutes = (seconds % 3600) / 60
      minutes = round(minutes)
      return '{hours}ч. {minutes}мин.'.format(hours=hours, minutes=minutes)

    def is_visit_long(self, duration, minutes=30):
      return round(duration.total_seconds()) > minutes * 60
