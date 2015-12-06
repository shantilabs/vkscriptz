# -*- coding: utf-8 -*-
import json
import os
from os.path import expanduser

import requests
import sys
import time



# def update_token(value):
#     credentials.access_token = value
#     credentials.save()


# def refresh_token():
#     resp = _get(
#         'https://oauth.vk.com/access_token',
#         client_id=credentials.client_id,
#         client_secret=credentials.client_secret,
#         grant_type='client_credentials',
#         redirect_uri='http://nothing.ru/',
#     )
#     sys.stderr.write('> {}\n'.format(repr(resp)))
#     update_token(resp['access_token'])


USER_FIELDS = (
    'sex',
    'bdate',
    'city',
    'country',
    'photo_50',
    'photo_100',
    'photo_200_orig',
    'photo_200',
    'photo_400_orig',
    'photo_max',
    'photo_max_orig',
    'online',
    'online_mobile',
    'lists',
    'domain',
    'has_mobile',
    'contacts',
    'connections',
    'site',
    'education',
    'universities',
    'schools',
    'can_post',
    'can_see_all_posts',
    'can_see_audio',
    'can_write_private_message',
    'status',
    'last_seen',
    # 'common_count',
    'relation',
    'relatives',
    'counters',
)


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


def vk_instagrams(group_id):
    for item in paginate(
        'https://api.vk.com/method/groups.getMembers',
        1000,
        group_id=group_id,
        fields='connections',
    ):
        if 'instagram' in item:
            yield item['instagram']


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
