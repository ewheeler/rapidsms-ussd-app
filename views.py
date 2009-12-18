#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import codecs
import csv

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext

from rapidsms.webui.utils import render_to_response, paginated
from ussd.models import *

from utilities.export import export

def index(req):
    return render_to_response(req,
        "ussd/index.html", {
            "sims" : SIM.objects.all(),
            "transfers" : AirtimeTransfer.objects.all()
        })

def bulk_airtime(req):
    file = req.FILES['file']
    amount = req.POST['amount']
    sim = SIM.objects.get(pk=int(req.POST['sim']))

    # use codecs.open() instead of open() so all characters are utf-8 encoded
    # BEFORE we start dealing with them (just in case)
    # rU option is for universal-newline mode which takes care of \n or \r etc
    #csvee = codecs.open(file, "rU", encoding='utf-8', errors='ignore')
    csvee = file

    # sniffer attempts to guess the file's dialect e.g., excel, etc
    dialect = csv.Sniffer().sniff(csvee.read(1024))
    csvee.seek(0)
    # DictReader uses first row of csv as key for data in corresponding column
    #reader = csv.DictReader(csvee, dialect=dialect)

    reader = csv.DictReader(csvee, quoting=csv.QUOTE_ALL, dialect=dialect)

    sent_to = []
    try:
        for row in reader:
            if row.has_key('NUMERO'):
                if row['NUMERO'] != "":
                    print(row['NUMERO'])
                    # cast as strings
                    trans = AirtimeTransfer(destination=str(row['NUMERO']),\
                        amount=amount, status='Q', sim=sim)
                    trans.save()
                    sent_to.append(trans)
                    continue

    except csv.Error, e:
        # TODO handle this error?
        print('%d : %s' % (reader.reader.line_num, e))
    return HttpResponseRedirect("/ussd")

def csv_transfers(req, format='csv'):
    return export(AirtimeTransfer.objects.all())
    #return export(AirtimeTransfer.objects.all(), [])
