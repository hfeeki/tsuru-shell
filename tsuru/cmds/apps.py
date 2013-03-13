#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from requests.exceptions import ConnectionError
from tsuru.utils import error, login_required, ExpHandler

def myhandler(e):
    print 'Caught exception!', e

class AppManager(object):
    """
    Manage App resources.
    """

    def __init__(self, target, dbn):
        self.target = target
        self.dbn = dbn  # must set it, login_required will use it

    @login_required
    @ExpHandler((ConnectionError, Exception))
    def list(self):
        """
        Get a list of all apps.
        """
        response = requests.get(
            "{0}/apps".format(self.target),
            headers = self.auhd
        )
        return response.content

    @login_required
    @ExpHandler((ConnectionError, Exception))
    def get(self, appname):
        """
        show information about your app.
        """
        response = requests.get(
            "{0}/apps/{1}".format(self.target, appname),
            headers = self.auhd
        )
        if response.ok:
            # print app info
            pass
        else:
            print("Failed to get app info.\nReason: %s" % (response.content))
        return response.content

    @login_required
    @ExpHandler((ConnectionError, Exception))
    def remove(self, appname):
        """
        Remove an app.
        """
        response = requests.delete(
            "{0}/apps/{1}".format(self.target, appname),
            headers = self.auhd
        )
        if response.ok:
            print("Successfully remove an app.")
        else:
            print("Failed to remove an app.\nReason: %s" % (response.content))
        return 

    @login_required
    @ExpHandler((ConnectionError, Exception))
    def create(self, name, framework, numunits=1):
        """
        Create an app.
        """
        data = {
            "name": name,
            "framework": framework,
            "units": numunits
        }
        response = requests.post(
            "{0}/apps".format(self.target),
            data=json.dumps(data),
            headers = self.auhd
        )
        if response.ok:
            print("Successfully created an app.")
        else:
            print("Failed to create an app.\nReason: %s" % (response.content))
        return response.content

    @login_required
    @ExpHandler((ConnectionError, Exception))
    def unitadd(self, appname, numunits=1):
        """
        Add a new unit to an app.
        """
        response = requests.put("{0}/apps/{1}/units".format(self.target, appname), data=str(numunits))
        if response.ok:
            print("Successfully add units to an app.")
        else:
            print("Failed to add units to an app.\nReason: %s" % (response.content))
        return response.content

    @login_required
    @ExpHandler((ConnectionError, Exception))
    def unitremove(self, appname, numunits=1):
        """
        Remove units from an app.
        """
        response = requests.delete("{0}/apps/{1}/units".format(self.target, appname), data=str(numunits))
        if response.ok:
            print("Successfully remove units from an app.")
        else:
            print("Failed to remove units from an app.\nReason: %s" % (response.content))
        return response.content

    @login_required
    @ExpHandler((ConnectionError, Exception))
    def envget(self):
        '''Retrieve environment variables for an app. If you don't provide the app name, tsuru will try to guess it.\n
        '''
        error("Not implemented!")
        

