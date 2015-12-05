# -*- coding: utf-8 -*-
import os

import requests
import sys
import time


coding = sys.stdout.encoding or sys.stdin.encoding
root = os.path.realpath(os.path.dirname(__file__))

CLIENT_ID = 5170022
CLIENT_SECRET = 'tr1910mxsP9PIvsBaByQ'
VERSION_ID = '5.40'


ACCESS_TOKEN = ''
access_token_txt = os.path.join(root, 'access_token.txt')
if os.path.exists(access_token_txt):
    ACCESS_TOKEN = open(access_token_txt).read().strip()


def update_token(value):
    global ACCESS_TOKEN
    ACCESS_TOKEN = value
    open(access_token_txt, 'w').write(value)


def refresh_token():
    resp = _get(
        'https://oauth.vk.com/access_token',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        grant_type='client_credentials',
        redirect_uri='http://nothing.ru/',
    )
    sys.stderr.write('> {}\n'.format(repr(resp)))
    update_token(resp['access_token'])


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


def vk_wall(owner_id):
    """
    https://vk.com/dev/wall.get
    """
    for item in paginate(
        'https://api.vk.com/method/wall.get',
        100,
        owner_id=owner_id,
    ):
        yield item


def vk_info(user_ids):
    """
    https://vk.com/dev/users.get
    """
    if not hasattr(user_ids, '__iter__'):
        user_ids = [user_ids]
    user_ids = map(str, user_ids)
    chunk_size = 100
    for offset in xrange(0, len(user_ids), chunk_size):
        cur_ids = user_ids[offset:offset + chunk_size]
        for item in list_request(
            'https://api.vk.com/method/users.get',
            user_ids=','.join(cur_ids),
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
    if not hasattr(user_ids, '__iter__'):
        user_ids = [user_ids]
    user_ids = map(str, user_ids)
    chunk_size = 100
    for offset in xrange(0, len(user_ids), chunk_size):
        cur_ids = user_ids[offset:offset + chunk_size]
        for item in list_request(
            'https://api.vk.com/method/groups.isMember',
            group_id=group_id,
            user_ids=','.join(cur_ids),
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
        access_token=ACCESS_TOKEN,
    )
    return 'response' in resp and resp['response'] == 1


def vk_likes(owner_id, type, item_id):
    """
    https://vk.com/dev/likes.getList
    """
    assert type in (
        'post',
        'comment',
        'photo',
        'audio',
        'video',
        'note',
        'photo_comment',
        'video_comment',
        'topic_comment',
        'sitepage',
    )
    for item in paginate(
        'https://api.vk.com/method/likes.getList',
        100,
        owner_id=owner_id,
        item_id=item_id,
        type=type,
    ):
        yield item


def vk_wall_comments(owner_id, post_id, preview_length=0):
    """
    https://vk.com/dev/wall.getComments
    """
    for item in paginate(
        'https://api.vk.com/method/wall.getComments',
        100,
        owner_id=owner_id,
        post_id=post_id,
        preview_length=preview_length,
    ):
        yield item


def vk_group_members(group_id, city_id=None):
    """
    https://vk.com/dev/groups.getMembers
    """
    if city_id:
        city_id = int(city_id)
    for item in paginate(
        'https://api.vk.com/method/groups.getMembers',
        1000,
        group_id=group_id,
        fields='city' if city_id else '',
    ):
        if city_id:
            if 'city' in item and item['city']['id'] == city_id:
                yield item['id']
        else:
            yield item


def vk_instagrams(group_id):
    for item in paginate(
        'https://api.vk.com/method/groups.getMembers',
        1000,
        group_id=group_id,
        fields='connections',
    ):
        if 'instagram' in item:
            yield item['instagram']


def vk_user_groups(user_id):
    for item in paginate(
        'https://api.vk.com/method/groups.get',
        1000,
        user_id=user_id,
        extended=1,
        fields='name,screen_name',
        access_token=ACCESS_TOKEN,
    ):
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
):
    """
    https://vk.com/dev/groups.search
    """
    for item in paginate(
        'https://api.vk.com/method/groups.search',
        1000,
        q=q,
        type=type,
        country_id=country_id,
        city_id=city_id,
        future=future,
        sort=sort,
        access_token=ACCESS_TOKEN,
    ):
        yield item


def has_tmp_error(response):
    return 'error' in response and response['error']['error_msg'].startswith((
        'Too many requests',
        'Internal server error',
    ))


def has_access_error(response):
    return 'error' in response and response['error']['error_msg'].startswith((
        'Access denied',
        'Access to group denied',
        'Permission to perform this action is denied',
    ))


def _get(url, **params):
    while 1:
        resp = requests.get(url, params=dict(
            params, v=VERSION_ID,
        ))
        # sys.stderr.write("> GET {} with {}: -> '{}'".format(
        #     url,
        #     repr(params),
        #     resp.text,
        # ))
        data = resp.json()
        if has_tmp_error(data):
            time.sleep(.5)
            continue
        break
    if has_access_error(data):
        sys.stderr.write(resp.text)
        raise Exception("access error: %s" % str(data['error']))
    return data


def paginate(url, count, **params):
    for offset in xrange(0, sys.maxint, count):
        if 'access_token' in params:
            time.sleep(.5)
        data = _get(url, **dict(params, offset=offset, count=count))
        try:
            items = data['response']['items']
        except:
            sys.stderr.write("no items in data: %s" % str(data))
            raise
        if not items:
            break
        for item in items:
            yield item


def list_request(url, **params):
    data = _get(url, **params)
    try:
        items = data['response']
    except:
        sys.stderr.write("no response in data: %s" % str(data))
        raise
    for item in items:
        yield item


def format_dict(d):
    return '\t'.join('{}={}'.format(k, v or '""') for k, v in d.items())
