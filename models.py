#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import re
from datetime import datetime

from django.db import models

from reporters.models import PersistantBackend

class SIM(models.Model):
    operator_name = models.CharField(max_length=20, blank=True, null=True)
    backend = models.ForeignKey(PersistantBackend, blank=True, null=True)
    balance = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.operator_name, self.backend.slug)

class OperatorNotification(models.Model):
    NOTIFICATION_CHOICES = (
        ('U', 'Unknown'),
        ('R', 'Receive Airtime'),
        ('S', 'Transfer Success'),
        ('F', 'Transfer Failure'),
        ('B', 'Airtime Balance'),
    )
    text = models.CharField(max_length=160, blank=True, null=True)
    identity = models.CharField(max_length=160, blank=True, null=True)
    sim = models.ForeignKey(SIM)
    received = models.DateTimeField(default=datetime.now, blank=True, null=True)
    type = models.CharField(max_length=1, choices=NOTIFICATION_CHOICES, default='U')

    def __unicode__(self):
        return "%s: %s (%s)" % (self.sim.operator_name, self.get_type_display(), self.received)

class AirtimeTransaction(models.Model):
    TRANS_RESULT_CHOICES = (
        ('P', 'Pending'),
        ('S', 'Success'),
        ('F', 'Failure'),
        ('U', 'Unknown'),
    )
    sim = models.ForeignKey(SIM)
    amount = models.CharField(max_length=160, blank=True, null=True)
    result = models.CharField(max_length=1, choices=TRANS_RESULT_CHOICES, default='P')
    initiated = models.DateTimeField(blank=True, null=True)
    notification = models.ForeignKey(OperatorNotification, blank=True, null=True)

    def __unicode__(self):
        return "%s: %s CFA, %s" % (self.sim.operator_name, self.amount, self.get_result_display())

class AirtimeTransfer(AirtimeTransaction):
    destination = models.CharField(max_length=160, blank=True, null=True)

    @property
    def crux(self):
        return self.destination

class AirtimeRecharge(AirtimeTransaction):
    recharge_code = models.CharField(max_length=160, blank=True, null=True)

    @property
    def crux(self):
        return self.recharge_code
