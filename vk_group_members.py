#!/usr/bin/env python
from __future__ import unicode_literals
import requests
import sys


FIELDS = (
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
    #'common_count',
    'relation',
    'relatives',
    'counters',
)


def vk_group_members(group_id, count=1000, fields=()):
    """
    https://vk.com/dev/groups.getMembers
    """
    for offset in xrange(0, sys.maxint, count):
        users = requests.get('https://api.vk.com/method/groups.getMembers', params=dict(
            group_id=group_id,
            offset=offset,
            count=count,
            fields=','.join(fields),
        )).json()['response']['users']
        if not users:
            break
        for user in users:
            yield user


if __name__ == '__main__':
    fields = [
        'city',
        'online',
    ]
    for group_id in sys.argv[1:]:
        for user in vk_group_members(group_id, fields=fields):
            if fields:
                print '\t'.join('{}={}'.format(k, v or '""') for k, v in user.items()).encode('utf-8')
            else:
                print user

