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

class AirtimeTransaction(models.Model):
    sim = models.ForeignKey(SIM)
    amount = models.CharField(max_length=160)
    confirmed = models.DateTimeField(blank=True,null=True)

class AirtimeTransfer(AirtimeTransaction):
    destination = models.CharField(max_length=160)
    initiated = models.DateTimeField(blank=True,null=True)

    @property
    def crux(self):
        return self.destination

class AirtimeRecharge(AirtimeTransaction):
    recharge_code = models.CharField(max_length=160)

    @property
    def crux(self):
        return self.recharge_code
