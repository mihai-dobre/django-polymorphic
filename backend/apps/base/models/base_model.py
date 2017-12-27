import json

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from service import Service


class BaseRequest(models.Model):
    VALID_STATUSES = [
        ('accepted', 'accepted'),
        ('queued', 'queued'),
        ('sending', 'sending'),
        ('sent', 'sent'),
        ('receiving', 'receiving'),
        ('received', 'received'),
        ('delivered', 'delivered'),
        ('undelivered', 'undelivered'),
        ('failed', 'failed'),
    ]

    QUEUES = [
        (1, 'priority'),
        (2, 'other'),
        (3, 'sms_box'),
    ]

    VALID_INFRASTRUCTURES = [
        (1, 'twilio'),
        (2, 'smsbox1'),
        (3, 'smsbox2')
    ]
    user = models.ForeignKey(User)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    recipient_phone_number = models.CharField(validators=[phone_regex], max_length=15) # validators should be a list
    country = models.CharField(max_length=64, blank=True, null=True)
    msg = models.CharField(max_length=1600)
    msg_sid = models.CharField(max_length=64, blank=True, null=True)
    timestamp_send = models.DateTimeField(auto_now_add=True)
    timestamp_confirmation = models.DateTimeField(blank=True, null=True)
    # queue = models.CharField(choices=QUEUES, max_length=32, blank=True)
    # general status and message set by twilio using the callback url
    status = models.CharField(max_length=32, choices=VALID_STATUSES, blank=True, null=True)
    service_response = models.CharField(max_length=1024, blank=True, null=True)
    # the service used to send the sms/voice
    service = models.ForeignKey(Service, default=None, related_name='service')
    infrastructure_used = models.CharField(max_length=32, choices=VALID_INFRASTRUCTURES, blank=True, null=True)

    class Meta:
        abstract = True
        permissions = (
            ("view", "Can view data"),
            )

    def __str__(self):
        return '{} - {}'.format(self.recipient_phone_number, self.msg)

    def __unicode__(self):
        return '{} - {}'.format(self.recipient_phone_number, self.msg)