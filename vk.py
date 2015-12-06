#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import sys
import urllib
import webbrowser
from os.path import expanduser

import click

from vkscriptz_core.api import VkApi
from vkscriptz_core.credentials import JsonCredentials


home = expanduser('~')
credentials = JsonCredentials(os.path.join(home, '.vkscriptz.json'))
vk = VkApi(credentials)
coding = sys.stdout.encoding or sys.stdin.encoding


def write(s):
    sys.stderr.write(s.encode(coding))


@click.group()
def main():
    pass


@main.command(help='Создать токен для доступа')
def auth():
    webbrowser.open('https://oauth.vk.com/authorize?' + urllib.urlencode(dict(
        client_id=credentials.client_id,
        redirect_uri='https://api.vk.com/blank.html#',
        display='page',
        scope='offline,ads,messages,friends',
        # response_type='code',
        response_type='token',
        v=vk.VERSION_ID,
    )))
    write('Браузер должен открыть страницу "https://api.vk.com/blank.html'
          '#access_token=<многобукв>". Надо скопировать все <многобукв> '
          'сюда, и нажать ENTER\n')
    result = raw_input('>').strip().split('&')[0]
    if result:
        credentials.access_token = result
        credentials.save()
        write('отлично, сохранили всё в {}\n'.format(credentials.fname))
    else:
        write('не вышло? жалко :(\n')


@main.command(help='Группы пользователя/пользователей')
@click.argument('user_id', nargs=-1, required=True)
def user_groups(user_id):
    for user_id in user_id:
        write('user#{}: '.format(user_id))
        n = 0
        for item in vk.user_groups(user_id):
            write('{}\thttps://vk.com/{}\n'.format(
                item['id'],
                item['screen_name'],
            ))
            n += 1
        write('{} group(s)\n'.format(n))


if __name__ == '__main__':
    main()
