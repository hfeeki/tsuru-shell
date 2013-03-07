#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


class AppManager(object):
    """
    Manage App resources.
    """

    def __init__(self, target):
        self.target = target

    def list(self):
        """
        Get a list of all apps.
        """
        response = requests.get("{0}/apps".format(self.target))
        return response.json

    def get(self, appname):
        """
        show information about your app.
        """
        response = requests.get("{0}/apps/{1}".format(self.target, appname))
        return response.json

    def remove(self, appname):
        """
        Remove an app.
        """
        response = requests.delete("{0}/apps/{1}".format(self.target, appname))
        return response.json

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
            data=json.dumps(data)
        )
        return response.json

    def unit-add(self, appname, numunits=1):
        """
        Add a new unit to an app.
        """
        response = requests.put("{0}/apps/{1}/units".format(self.target, appname), data=str(numunits))
        return response.json

    def unit-remove(self, appname, numunits=1):
        """
        Remove units from an app.
        """
        response = requests.delete("{0}/apps/{1}/units".format(self.target, appname), data=str(numunits))
        return response.json

