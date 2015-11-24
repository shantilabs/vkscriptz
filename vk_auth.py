#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import urllib
import webbrowser

import requests

from _vkscriptz import CLIENT_ID, VERSION_ID, CLIENT_SECRET, update_token


if __name__ == '__main__':
    if len(sys.argv) == 1:
        webbrowser.open('https://oauth.vk.com/authorize?' + urllib.urlencode(dict(
            client_id=CLIENT_ID,
            redirect_uri='https://api.vk.com/blank.html#',
            display='page',
            scope='offline,ads,messages,friends',
            # response_type='code',
            response_type='token',
            v=VERSION_ID,
        )))
        # print('Открылась страница https://api.vk.com/blank.html#code=xxxxxxxx')
        # print('Теперь надо запустить команду "{} xxxxxxxx"'.format(sys.argv[0]))
    # else:
    #     code = sys.argv[0]
    #     resp = requests.get(
    #         'https://oauth.vk.com/access_token',
    #         params=dict(
    #             client_id=CLIENT_ID,
    #             client_secret=CLIENT_SECRET,
    #             v=VERSION_ID,
    #             grant_type='client_credentials',
    #             code=code,
    #         ),
    #     )
    #     update_token(resp.json()['access_token'])
    #     print('Получилось. Теперь можно делать запросы.')
