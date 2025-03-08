from django.db import models

class SMSMessage(models.Model):
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    body = models.TextField()
    timestamp = models.DateTimeField()
    message_type = models.CharField(max_length=10)  # 'sms' or 'mms'
    delivery = models.CharField(max_length=20, blank=True, null=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"SMS from {self.sender} at {self.timestamp}"