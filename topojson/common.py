# coding: utf-8

import json

class Arc(object):

    def __init__(self, index_a, index_b):

        self.a = index_a
        self.b = index_b
        self.next = None
        self.count = 0

def copy_key(instance, receiver, *keys):

    for key in keys:
        if instance.has_key(key) and instance[key]:

            receiver[key] = json.loads(json.dumps(instance[key]))