#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.contrib import admin 
from ussd.models import *

class SIMAdmin(admin.ModelAdmin):
    list_display = ('operator_name', 'backend', 'balance')

admin.site.register(OperatorNotification)
admin.site.register(AirtimeTransaction)
admin.site.register(AirtimeTransfer)
admin.site.register(AirtimeRecharge)
admin.site.register(SIM, SIMAdmin)
