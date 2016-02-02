import os
import json


class JsonCredentials(object):
    keys = (
        'client_id',
        'client_secret',
        'access_token',
    )

    def __init__(self, fname):
        self.fname = fname
        if not os.path.exists(fname):
            self.client_id = 5161445
            self.client_secret = 'l6bLNsD6jvOwBpWZOxQG'
            self.access_token = ''
            self.save()
        self.load()

    def load(self):
        with open(self.fname) as f:
            for k, v in json.load(f).items():
                if k in self.keys:
                    setattr(self, k, v)

    def save(self):
        with open(self.fname, 'w') as f:
            json.dump({k: getattr(self, k) for k in self.keys}, f)
