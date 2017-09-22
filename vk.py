#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import sys
import urllib
import webbrowser
from collections import Counter
from os.path import expanduser

import click

from core.api import VkApi
from core.credentials import JsonCredentials
from core.errors import AccessTokenRequired, AccessError


home = expanduser('~')
credentials = JsonCredentials(os.path.join(home, '.vkscriptz.json'))
vk = VkApi(credentials)
coding = sys.stdout.encoding or sys.stdin.encoding
logging.basicConfig(level=logging.WARN, stream=sys.stderr)


def stderr(s):
    sys.stderr.write(s.encode(coding))


def stdout(s):
    sys.stdout.write(s.encode(coding))


def force_group_id(gid):
    if gid.isdigit():
        gid = int(gid)
    else:
        name = gid
        gid = vk.group_info(gid)['id']
        stderr('Group {} resolved to ID {}\n'.format(name, gid))
    return gid


def force_user_id(uid):
    if isinstance(uid, basestring) and not uid.isdigit():
        name = uid
        user = next(vk.user_info(uid), None)
        if not user:
            stderr('Unknown user {}\n'.format(uid))
            sys.exit(1)
        uid = ['id']
        stderr('User {} resolved to ID {}\n'.format(name, uid))
    return uid


@click.group()
def main():
    pass


@main.command(help='Создать токен для доступа')
def auth():
    webbrowser.open('https://oauth.vk.com/authorize?' + urllib.urlencode(dict(
        client_id=credentials.client_id,
        redirect_uri='https://api.vk.com/blank.html#',
        display='page',
        scope=','.join((
            'offline',
            'ads',
            'messages',
            'friends',
            'groups',
            'stats',
            'wall',
        )),
        # response_type='code',
        response_type='token',
        v=vk.VERSION_ID,
    )))
    stderr('Браузер должен открыть страницу "https://api.vk.com/blank.html'
           '#access_token=<многобукв>". Надо скопировать все <многобукв> '
           'сюда, и нажать ENTER\n')
    result = raw_input('>').strip().split('&')[0]
    if result:
        credentials.access_token = result
        credentials.save()
        stderr('отлично, сохранили всё в {}\n'.format(credentials.fname))
    else:
        stderr('не вышло? жалко :(\n')


@main.command(help='Группы пользователя')
@click.argument('user_id', nargs=-1, required=True)
def user_groups(user_id):
    for user_id in map(force_user_id, user_id):
        stderr('user#{}: '.format(user_id))
        n = 0
        try:
            for item in vk.user_groups(user_id):
                stdout('{}\thttps://vk.com/{}\n'.format(
                    item['id'],
                    item['screen_name'],
                ))
                n += 1
        except AccessError:
            stderr('error: private group list\n')
            continue
        stderr('{} group(s)\n'.format(n))


@main.command(help='Поиск групп по названиям (до 1000 групп)')
@click.argument('query', nargs=1, required=True)
@click.option('--country_id', default=1, help='ID страны', type=int)
@click.option('--city_id', default=None, help='ID города', type=int)
def group_search(query, country_id, city_id):
    for item in vk.group_search(query, country_id=country_id, city_id=city_id):
        stdout('{}\t{}\n'.format(
            item['id'],
            item['name'].replace('\n', ' '),
        ))


@main.command(help='Участники групп')
@click.argument('group_id', nargs=-1, required=True)
@click.option('--city_id', default=None, help='ID города', type=int)
@click.option('--dead', default=False, help='Только мёртвые', is_flag=True)
@click.option('--min-intersection', default=1,
              help='Участники минимум N групп', type=int)
def group_members(group_id, city_id, dead, min_intersection):
    num_groups = len(group_id)
    if min_intersection == 0:
        min_intersection = num_groups
    counter = Counter() if num_groups > 1 else None
    for group_id in map(force_group_id, group_id):
        stderr('group#{}: '.format(group_id))
        n = 0
        try:
            for item in vk.group_members(group_id):
                if city_id and (
                    'city' not in item or
                    item['city']['id'] != city_id
                ):
                    continue
                if dead and 'deactivated' not in item:
                    continue
                uid = item['id']
                if counter is None:
                    stdout('{}\n'.format(uid))
                else:
                    counter[uid] += 1
                n += 1
        except AccessError:
            stderr('error: private group\n')
            continue
        stderr('{} member(s)\n'.format(n))
    if counter is not None:
        for uid, num in sorted(counter.items(), key=lambda (k, v): (-v, k)):
            if min_intersection > 0 and num < min_intersection:
                continue
            stdout('{}\t{}\n'.format(uid, num))


@main.command(help='Инстаграмы участников групп')
@click.argument('group_id', nargs=-1, required=True)
@click.option('--city_id', default=None, help='ID города', type=int)
def group_members_instagrams(group_id, city_id):
    for group_id in map(force_group_id, group_id):
        stderr('group#{}: '.format(group_id))
        n = 0
        for item in vk.group_members(group_id):
            if city_id and (
                'city' not in item or
                item['city']['id'] != city_id
            ):
                continue
            if 'instagram' in item:
                stdout('https://www.instagram.com/{}/\n'.format(
                    item['instagram'],
                ))
                n += 1
        stderr('{} member(s)\n'.format(n))


# TODO: счётчики по количеству каментов
@main.command(help='Самые активные участники')
@click.argument('group_id', nargs=-1, required=True)
def group_active_members(group_id):
    for group_id in map(force_group_id, group_id):
        stderr('group#{}: '.format(group_id))
        n = 0
        gid = -group_id
        for post in vk.wall(gid):
            for like in vk.likes(gid, 'post', post['id']):
                if like > 0:
                    stdout('{}\n'.format(like))
                    n += 1
            for comment in vk.wall_comments(gid, post['id']):
                if comment['from_id'] > 0:
                    stdout('{}\n'.format(comment['from_id']))
                    n += 1
                for like in vk.likes(gid, 'comment', comment['id']):
                    stdout('{}\n'.format(like))
                    n += 1
        stderr('{} active member(s)\n'.format(n))


@main.command(help='Репосты')
@click.argument('group_id', nargs=1, required=True)
@click.argument('post_id', nargs=1, required=True)
def group_reposts(group_id, post_id):
    reposts = (
        item
        for item in vk.wall_reposts(force_group_id(group_id), post_id)
        if item['from_id'] > 0
    )
    for i, item in enumerate(reposts, start=1):
        stdout('{}. {}\n'.format(i, VkApi.user_link(item['from_id'])))


@main.command(help='Удаляет участников из группы')
@click.argument('group_id', nargs=1, required=True)
@click.argument('user_id', nargs=-1, required=False)
@click.option('--dead', default=False, help='Только мёртвые', is_flag=True)
def group_remove_members(group_id, user_id, dead):
    group_id = force_group_id(group_id)
    success, failed = (0, 0)
    if dead:
        user_id = list(user_id)
        for item in vk.group_members(group_id):
            if 'deactivated' in item:
                user_id.append(item['id'])
    for user_id in map(force_user_id, user_id):
        if vk.group_remove_member(group_id, user_id):
            success += 1
        else:
            failed += 1
    stderr('Success: {}, failed {}\n'.format(success, failed))


@main.command(help='Те, у кого друзья в группе')
@click.argument('group_id', nargs=1, required=True)
@click.option('--max_user_friends', default=1000, type=int)  # накрученные акки
@click.option('--min_friends_in_group', default=2, type=int)
@click.option('--human', default=False, type=bool, is_flag=True)
def friends_in_group(group_id, max_user_friends, min_friends_in_group, human):
    group_id = force_group_id(group_id)
    counter = Counter()
    members = []
    for i, member in enumerate(vk.group_members(group_id, skip_dead=True),
                               start=1):
        stderr('{}. https://vk.com/id{} '.format(i, member['id']))
        friends = list(vk.friends(member['id']))
        stderr('{} friend(s)\n'.format(len(friends)))
        if max_user_friends and len(friends) > max_user_friends:
            stderr('...skip\n')
            continue
        for friend in friends:
            counter[friend['id']] += 1
        members.append(member['id'])
    for member_id in members:
        counter.pop(member_id, None)
    for uid, num in sorted(counter.items(), key=lambda (k, v): (-v, k)):
        if num < min_friends_in_group:
            continue
        if human:
            stdout('https://vk.com/id{}\t{}\n'.format(uid, num))
        else:
            stdout('{}\n'.format(uid))


@main.command(help='Статистика слов на основе моих сообщений')
# если ~6-8 тыс. слов в день норма, то возьмём, скажем, 2 года
@click.option('--depth_words', nargs=1, default=7000*365*2, type=int)
@click.option('--min_word_length', nargs=1, default=3, type=int)
@click.option('--show_top_percent', nargs=1, default=80, type=int)
@click.option('--phrases', default=False, is_flag=True)
def my_dict(depth_words, min_word_length, show_top_percent, phrases=False):
    result = Counter()
    if phrases:
        stream = _phrases_stream()
    else:
        stream = _words_stream(min_word_length)
    for total, word in enumerate(stream):
        result[word] += 1
        if total > depth_words:
            break
    total_percent = 0
    unique_words = result.items()
    for i, (word, n) in enumerate(
        sorted(unique_words, key=lambda (word, n): -n),
        start=1,
    ):
        percent = float(n) / total
        total_percent += percent
        if total_percent * 100 >= show_top_percent:
            break
        stdout('#{}\t{:.0%}\t{} ({:.4%})\t\t{}\n'.format(
               i, total_percent, n, percent, word))
    stdout('--------------------------\n')
    stdout('найдено слов всего: {}\n'.format(total))
    stdout('из них разных: {}\n'.format(len(unique_words)))
    stdout('{}% текста это {:.0%} слов\n'.format(
        show_top_percent,
        float(i) / len(unique_words),
    ))


def _words_stream(min_word_length=None, use_pymorphy=True):
    if use_pymorphy:
        import pymorphy2
        morph = pymorphy2.MorphAnalyzer()
    else:
        morph = None
    abc = u'йцукенгшщзхъфывапролджэячсмитьбюё-'
    for item in vk.messages(out=True):
        s = item['body'].strip().lower()
        if not s:
            continue
        stderr('> {}\n'.format(s))
        for word in s.split():
            word = ''.join(char for char in word if char in abc).strip('-')
            if min_word_length:
                if len(word) < min_word_length or len(set(word)) < 2:
                    continue
            elif not word:
                continue
            if use_pymorphy:
                word = morph.parse(word)[0].normal_form
            yield word


def _phrases_stream():  # TODO: сделать лучше, сделать умней
    prev = None
    for word in _words_stream(use_pymorphy=False):
        if prev is not None:
            yield '{} {}'.format(prev, word)
        prev = word


@main.command(help='Авторы фото в альбоме')
@click.argument('group_id', nargs=1, required=True)
@click.argument('album_id', nargs=1, required=True)
@click.option('--is_group', default=True, type=bool)
def group_album_authors(group_id, album_id, is_group):
    group_id = force_group_id(group_id)
    if is_group:
        group_id *= -1
    result = {}
    for photo in vk.get_album_photos(group_id, album_id):
        link = VkApi.user_link(photo['user_id'])
        stderr('photo#{}: {}\n'.format(photo['id'], link))
        result[link] = 'https://vk.com/photo{}_{}'.format(group_id, photo['id'])
    for i, link in enumerate(result.values(), start=1):
        stdout('{}. {}\n'.format(i, link))


@main.command(help='Лайки к посту')
@click.argument('group_id', nargs=1, required=True)
@click.argument('post_id', nargs=1, required=True)
@click.option('--is_group', default=True, type=bool)
@click.option('--members_only', default=False, type=bool, is_flag=True)
def post_likes(group_id, post_id, members_only, is_group):
    group_id = force_group_id(group_id)
    if is_group:
        group_id *= -1

    if members_only:
        stderr('members: ')
        members = {x['id'] for x in vk.group_members(-group_id, skip_dead=False)}
        stderr('{}\n'.format(len(members)))
    else:
        members = set()

    c = Counter()
    likers = Counter()
    liked_comments = Counter()
    comments = {}
    for comment in vk.wall_comments(group_id, post_id):
        likes = list(vk.likes(group_id, 'comment', comment['id']))
        stderr('comment#{} - {}\n'.format(comment['id'], len(likes)))
        comments[comment['id']] = comment
        if members:
            likes = list(set(likes) & members)
            stderr('members: {}\n'.format(len(likes)))
        liked_comments[comment['id']] += len(likes)
        c[comment['from_id']] += len(likes)
        for like in likes:
            likers[like] += 1

    total = 0
    for i, (user_id, n) in enumerate(sorted(c.items(), key=lambda x: -x[1])):
        stdout('{}. {} - {}\n'.format(i + 1, VkApi.user_link(user_id), n))
        total += n

    print('TOP LIKERS')
    for i, (user_id, n) in enumerate(sorted(likers.items(), key=lambda x: -x[1])):  # noqa
        stdout('{}. {} - {}\n'.format(i + 1, VkApi.user_link(user_id), n))

    print()
    print('TOP COMMENTS')
    for i, (comment_id, n) in enumerate(sorted(liked_comments.items(), key=lambda x: -x[1])):  # noqa
        stdout('{}. {} - {}\n'.format(i + 1, n, comments[comment_id]['text'] or comments[comment_id]))  # noqa

    stdout('TOTAL: {}\n'.format(total))


@main.command(help='Статистика лайков в альбоме')
@click.argument('group_id', nargs=1, required=True)
@click.argument('album_id', nargs=1, required=True)
@click.option('--members_only', default=False, type=bool, is_flag=True)
@click.option('--is_group', default=True, type=bool)
def group_album_stat(group_id, album_id, members_only, is_group):
    group_id = force_group_id(group_id)
    if members_only:
        stderr('members: ')
        members = {x['id'] for x in vk.group_members(group_id, skip_dead=True)}
        stderr('{}\n'.format(len(members)))
    else:
        members = set()
    result = []
    if is_group:
        group_id *= -1
    for photo in vk.get_album_photos(group_id, album_id):
        stderr('photo#{}: '.format(photo['id']))
        likes = {x for x in vk.likes(group_id, 'photo', photo['id'])}
        if members_only:
            likes = likes & members
        stderr('{}\n'.format(len(likes)))
        result.append({
            'link': 'https://vk.com/photo{}_{}'.format(group_id, photo['id']),
            'n_likes': len(likes),
        })
    result.sort(key=lambda d: -d['n_likes'])
    for d in result:
        stdout('{link}\t{n_likes}\n'.format(**d))


if __name__ == '__main__':
    try:
        main()
    except AccessTokenRequired:
        stderr(u'Сначала запустите {} auth\n'.format(sys.argv[0]))
        sys.exit(1)
