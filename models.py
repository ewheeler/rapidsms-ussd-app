#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from django.db import models
from reporters.models import PersistantBackend
import re
from datetime import datetime

class SIM(models.Model):
    operator_name = models.CharField(max_length=20, blank=True, null=True)
    backend = models.ForeignKey(PersistantBackend, blank=True, null=True)
    balance = models.CharField(max_length=500, blank=True, null=True)
