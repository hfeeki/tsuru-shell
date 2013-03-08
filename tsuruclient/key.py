import json
import requests
from utils import login_required, readkey
from configs import KEY_FN

class KeyManager(object):

    def __init__(self, target):
        self.target = target        

    @login_required
    def remove(self):
        '''Remove your public key ($HOME/.ssh/id_rsa.pub by default).\nUsage: key-remove [path/to/key/file.pub]
        '''
        if not os.path.exists(KEY_FN):
            print("You don't have a public key\nTo generate a key use 'ssh-keygen' command\n")
            return 
        key = readkey()
        data = {
            'key': key
        }
        response = requests.delete(
            "{0}/users/keys".format(self.target),
            data = json.dumps(data),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print("Key successfully removed!")
        else:
            print("Key failed to remove!\nReason: %s" % response.content)
        return response.content

    @login_required
    def add(self):
        '''Add your public key ($HOME/.ssh/id_rsa.pub by default).\nUsage: key-add [path/to/key/file.pub]
        '''
        if not os.path.exists(KEY_FN):
            print("You don't have a public key\nTo generate a key use 'ssh-keygen' command\n")
            return 
        key = readkey()
        data = {
            'key': key
        }
        response = requests.post(
            "{0}/users/keys".format(self.target),
            data = json.dumps(data),
            headers = self.auhd # must use login_required
        )
        if response.ok:
            print("Key successfully added!")
        else:
            print("Key failed to add!\nReason: %s" % response.content)
        return response.content
