# -*- coding: utf-8 -*-
import json
import os
from os.path import expanduser

import requests
import sys
import time


def vk_are_members(group_id, user_ids):
    """
    https://vk.com/dev/groups.isMember
    """
    for cur_ids in _chunkize(user_ids):
        for item in list_request(
            'https://api.vk.com/method/groups.isMember',
            group_id=group_id,
            user_ids=','.join(map(str, cur_ids)),
            extended=1,
        ):
            yield item


def format_dict(d):
    return '\t'.join('{}={}'.format(k, v or '""') for k, v in d.items())
