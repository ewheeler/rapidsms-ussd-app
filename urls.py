#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.conf.urls.defaults import *
import ussd.views as views

urlpatterns = patterns('',
    url(r'^ussd$', views.index),
    url(r'^ussd/bulk?$', views.bulk_airtime),
)
