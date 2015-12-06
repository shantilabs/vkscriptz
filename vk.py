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
vk_api = VkApi(credentials)
coding = sys.stdout.encoding or sys.stdin.encoding


def writeln(s):
    sys.stderr.write((s + '\n').encode(coding))


@click.group()
def main():
    pass


@main.command(help='Генерирует токен для доступа')
def auth():
    webbrowser.open('https://oauth.vk.com/authorize?' + urllib.urlencode(dict(
        client_id=credentials.client_id,
        redirect_uri='https://api.vk.com/blank.html#',
        display='page',
        scope='offline,ads,messages,friends',
        # response_type='code',
        response_type='token',
        v=vk_api.VERSION_ID,
    )))
    writeln('Браузер должен открыть страницу "https://api.vk.com/blank.html'
            '#access_token=<многобукв>". Надо скопировать все <многобукв> '
            'сюда, и нажать ENTER')
    result = raw_input('>').strip().split('&')[0]
    if result:
        credentials.access_token = result
        credentials.save()
        writeln('отлично, сохранили всё в {}'.format(credentials.fname))
    else:
        writeln('не вышло? жалко :(')


if __name__ == '__main__':
    main()
