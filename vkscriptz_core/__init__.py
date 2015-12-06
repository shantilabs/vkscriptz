# -*- coding: utf-8 -*-
import json
import os
from os.path import expanduser

import requests
import sys
import time

def vk_info(user_ids):
    """
    https://vk.com/dev/users.get
    """
    for cur_ids in _chunkize(user_ids):
        for item in list_request(
            'https://api.vk.com/method/users.get',
            user_ids=','.join(map(str, cur_ids)),
        ):
            yield item


def vk_group_info(group_id):
    """
    https://vk.com/dev/groups.getById
    """
    for item in list_request(
        'https://api.vk.com/method/groups.getById',
        group_id=group_id,
    ):
        return item


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


def vk_group_remove_member(group_id, user_id):
    """
    https://vk.com/dev/groups.removeUser
    """
    resp = _get(
        'https://api.vk.com/method/groups.removeUser',
        group_id=group_id,
        user_id=user_id,
        access_token=credentials.access_token,
    )
    return 'response' in resp and resp['response'] == 1


def list_request(url, **params):
    data = _get(url, **params)
    try:
        items = data['response']
    except:
        sys.stderr.write("no response in data: {}".format(data))
        raise
    for item in items:
        yield item


def _chunkize(ids, chunk_size=100):
    if not hasattr(ids, '__iter__'):
        ids = [ids]
    for offset in xrange(0, len(ids), chunk_size):
        yield ids[offset:offset + chunk_size]


def format_dict(d):
    return '\t'.join('{}={}'.format(k, v or '""') for k, v in d.items())
