#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from __future__ import with_statement
try:
    # NOTE Python 2.5 requires installation of simplejson library
    # http://pypi.python.org/pypi/simplejson
    import simplejson as json
except ImportError:
    # Python 2.6 includes json library
    import json

import rapidsms
from ussd.models import *

"""
    Example JSON object describing a mobile network
    {
        "Country Name":"Senegal",
        "Country Code":"SN",
        "Operator Short":"ORANGE SN",
        "Operator Numeric":"60801",
        "USSD Balance":"#123#",
        "USSD Transfer":"#116*1*%(destination)d*%(amount)d*%(PIN)d#",
        "Subscriber Pattern":"^(\+?221|0)(77)\d{7}$"
    }

    "Country Name" is human-friendly, "Country Code" is ISO country code,
    "Operator Short" is the human-friendly 'short alphanumeric' name returned
    by AT+COPS?, "Operator Numeric" is the 'numeric' name returned by AT+COPS
    and is globally unique (in MCC/MNC format where first 3 digits give country
    code and last two give network code), "USSD Balance" is the USSD string
    for checking airtime balance, "USSD Transfer" is the USSD string for
    transferring airtime credit with labled string substitutions for 
    destination (phone number credit is to be sent to), amount (amount of airtime
    or currency units), and PIN, "Subscriber Pattern" is a regular expression
    that will match fully-qualified (with country code prefix) or locally-
    originated numbers for all of the operator's number blocks.
"""
class App (rapidsms.app.App):
    def start(self):
        # TODO OS agnostic!
        mobile_networks_file = 'apps/ussd/mobile_networks.json'
        with open(mobile_networks_file, 'r') as f:
            setattr(self, "mobile_networks", json.load(f))

    def parse(self, message):
        pass

    def _run_ussd(self, backend_slug, ussd_string):
        backend = self.router.get_backend(backend_slug)
        return backend._Backend__run_ussd(ussd_string)

    def _get_network(self, field, search):
        for network in self.mobile_networks:
            f = network.get(field)
            if f is not None:
                if f == search:
                    return network

    def update_balance(self):
        sims = SIM.objects.all()
        balances = []
        for sim in sims:
            b = self.check_balance(sim.backend.slug, sim.operator_name)
            sim.balance = unicode(b)
            sim.save()
            balances.append(unicode(b))
        return balances

    def check_balance(self, backend_slug, operator_short):
        self.debug('checking balance...')
        network = self._get_network("Operator Short", operator_short)
        # TODO check for None
        result = self._run_ussd(backend_slug, network["USSD Balance"])
        if result is not None:
            self.debug(result)
            if len(result) == 1:
                result = result[0]
            return result

    def transfer_airtime(self, backend_slug, operator_short, destination, amount, pin):
        network = self._get_network("Operator Short", operator_short)
        ussd_string = network["USSD Transfer"] % {'destination' : destination,\
            'amount' : amount, 'PIN' : pin }
        result = self._run_ussd(backend_slug, ussd_string)
        if result is not None:
            self.debug(result)
            if len(result) == 1:
                result = result[0]
            return result

    def send_ro_credit(self):
        sim = SIM.objects.all()[0]
        return self.transfer_airtime(sim.backend.slug, sim.operator_name,\
            "772720297", "100", "")

    def handle(self, message):
        if message.text.lower().startswith("balance"):
            return message.respond(self.update_balance())
        if message.text.lower().startswith("send"):
            return message.respond(self.send_ro_credit())
