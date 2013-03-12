# -*- coding: utf-8 -*-
#!/usr/bin/env python


import os
import string
import json
import requests
from libs.utils import login_required, readkey
from common.configs import KEY_FN

class ServiceManager(object):

    def __init__(self, target):
        self.target = target  

    def _guessAppName(self):
        return None

    def create(self, fn):
        '''Creates a service based on a passed manifest. 
        The manifest format should be a yaml and follow the 
        standard described in the documentation 

        Usage:
            create path/to/manifesto
        '''
        with open(fn) as f:
            body = f.read()
        response = requests.post(
            "{0}/services".format(self.target),
            data=body
        )
        if response.ok:
            pass
        else:
            pass


    def list(self):
        '''Get all available services, and user's instances for this services
        '''
        # http GET http://192.168.33.10:8080/services/instances authorization:TOKEN
        response = requests.get(
            "{0}/services".format(self.target),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print(response.content)
            #print("Key successfully removed!")
        else:
            print("Get services list failed!\nReason: %s" % response.content)
        return response.content

    @login_required
    def add(self, servicename, instancename): 
        '''Create a service instance to one or more apps make use of.

        Usage: 
            service-add <servicename> <instancename>

            e.g.:
                $ tsuru service_add mongodb tsuru_mongodb

            Will add a new instance of the "mongodb" service, named "tsuru_mongodb".
        '''
        data = {
            "name": instancename,
            "service_name": servicename
        }
        response = requests.post(
            "{0}/services/instances".format(self.target),
            data=json.dumps(data),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print("Add a new instance: %s of the service: %s successfully!" % (instancename, servicename))
        else:
            print("Add new service instance failed!\nReason: %s" % response.content)
        return response.content

    @login_required
    def bind(self, instancename, appname):
        '''Bind a service instance to an app.
        '''
        response = requests.put(
            "{0}/services/instances/{1}/{2}".format(self.target, instancename, appname),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print("Instance %s successfully binded to the app %s." % (instancename, appname))
            print('''The following environment variables are now available for use in your app:\n- %s\nFor more details, please check the documentation for the service, using service-doc command.''' % string.join(response.json(), "\n "))
            #print("Key successfully removed!")
        else:
            print("Instance bind failed!\nReason: %s" % response.content)
        return response.content

    @login_required
    def unbind(self, instancename, appname):
        '''Unbind a service instance from an app
        '''
        response = requests.delete(
            "{0}/services/instances/{1}/{2}".format(self.target, instancename, appname),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print("Instance %s successfully unbinded from the app %s." % (instancename, appname))
        else:
            print("Unbind failed!\nReason: %s" % response.content)
        return response.content

    @login_required
    def status(self, instancename):
        '''Check status of a given service instance.
        '''
        # http GET http://192.168.33.10:8080/services/instances authorization:TOKEN
        response = requests.get(
            "{0}/services/instances/{1}/status".format(self.target, instancename),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print(response.content)
            #print("Key successfully removed!")
        else:
            print("Get service status failed!\nReason: %s" % response.content)
        return response.content

    @login_required
    def info(self, servicename):
        '''List all instances of a service.
        '''
        # http GET http://192.168.33.10:8080/services/instances authorization:TOKEN
        response = requests.get(
            "{0}/services/{1}".format(self.target, servicename),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print(response.content)
            #print("Key successfully removed!")
        else:
            print("Get service status failed!\nReason: %s" % response.content)
        return response.content


    @login_required
    def doc(self, servicename):
        '''Show documentation of a service.
        '''
        # http GET http://192.168.33.10:8080/services/instances authorization:TOKEN
        response = requests.get(
            "{0}/services/c/{1}/doc".format(self.target, servicename),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print(response.content)
            #print("Key successfully removed!")
        else:
            print("Get service doc failed!\nReason: %s" % response.content)
        return response.content


    @login_required
    def remove(self, instancename):
        '''Removes a service instance
        '''
        response = requests.delete(
            "{0}/services/c/instances/{1}".format(self.target, instancename),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print("Instance %s successfully removed." % (instancename))
        else:
            print("Remove service instance failed!\nReason: %s" % response.content)
        return response.content