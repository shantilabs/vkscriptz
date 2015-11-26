# -*- coding: utf-8 -*-
import os

import requests
import sys

import time

coding = sys.stdout.encoding or sys.stdin.encoding
root = os.path.realpath(os.path.dirname(__file__))
code_txt = os.path.join(root, 'access_token.txt')

CLIENT_ID = 5161445
CLIENT_SECRET = 'l6bLNsD6jvOwBpWZOxQG'
VERSION_ID = '5.40'
ACCESS_TOKEN = open(code_txt).read().strip() if os.path.exists(code_txt) else ''


def update_token(value):
    global ACCESS_TOKEN
    ACCESS_TOKEN = value
    open(code_txt, 'w').write(value)


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


def vk_wall(owner_id, count=100):
    """
    https://vk.com/dev/wall.get
    """
    for offset in xrange(0, sys.maxint, count):
        resp = requests.get('https://api.vk.com/method/wall.get', params=dict(
            owner_id=owner_id,
            offset=offset,
            count=count,
            # access_token=ACCESS_TOKEN,
            v=VERSION_ID,
        ))
        data = resp.json()
        # if 'error' in data and data['error']['error_msg'].startswith((
        #     'Access denied',
        #     'Access to group denied',
        # )):
        #     break
        try:
            items = data['response']['items']
        except:
            sys.stderr.write(resp.text)
            raise
        # time.sleep(.1)
        if not items:
            break
        for item in items:
            yield item


def vk_wall_comments(owner_id, post_id, preview_length=0, count=100):
    """
    https://vk.com/dev/wall.getComments
    """
    for offset in xrange(0, sys.maxint, count):
        resp = requests.get('https://api.vk.com/method/wall.getComments', params=dict(
            owner_id=owner_id,
            post_id=post_id,
            offset=offset,
            count=count,
            preview_length=preview_length,
            # access_token=ACCESS_TOKEN,
            v=VERSION_ID,
        ))
        data = resp.json()
        # if 'error' in data and data['error']['error_msg'].startswith((
        #     'Access denied',
        #     'Access to group denied',
        # )):
        #     break
        try:
            items = data['response']['items']
        except:
            sys.stderr.write(resp.text)
            raise
        # time.sleep(.1)
        if not items:
            break
        for item in items:
            yield item


def vk_group_members(group_id, city_id=None, count=1000):
    """
    https://vk.com/dev/groups.getMembers
    """
    if city_id:
        city_id = int(city_id)
    for offset in xrange(0, sys.maxint, count):
        resp = requests.get('https://api.vk.com/method/groups.getMembers', params=dict(
            group_id=group_id,
            offset=offset,
            count=count,
            fields='city' if city_id else '',
            # access_token=ACCESS_TOKEN,
            v=VERSION_ID,
        ))
        data = resp.json()
        if 'error' in data and data['error']['error_msg'].startswith((
            'Access denied',
            'Access to group denied',
        )):
            break
        try:
            items = data['response']['items']
        except:
            sys.stderr.write(resp.text)
            raise
        time.sleep(.5)
        if not items:
            break
        for item in items:
            if city_id:
                if 'city' in item and item['city']['id'] == city_id:
                    yield item['id']
            else:
                yield item


def vk_group_search(
    q,
    type=None,
    country_id=None,
    city_id=None,
    future=None,
    sort=0,
    # 0 — по умолчанию (аналогично результатам поиска в полной версии сайта);
    # 1 — по скорости роста;
    # 2 — по отношению дневной посещаемости к количеству пользователей;
    # 3 — по отношению количества лайков к количеству пользователей;
    # 4 — по отношению количества комментариев к количеству пользователей;
    # 5 — по отношению количества записей в обсуждениях к кол-ву пользователей.
    count=1000,
):
    """
    https://vk.com/dev/groups.search
    """
    resp = requests.get('https://api.vk.com/method/groups.search', params=dict(
        q=q,
        type=type,
        country_id=country_id,
        city_id=city_id,
        future=future,
        sort=sort,
        access_token=ACCESS_TOKEN,
        v=VERSION_ID,
        count=1000,
    ))
    try:
        items = resp.json()['response']['items']
    except:
        sys.stderr.write(resp.text)
        raise
    for item in items:
        yield item
    time.sleep(.5)


def format_dict(d):
    return '\t'.join('{}={}'.format(k, v or '""') for k, v in d.items())
