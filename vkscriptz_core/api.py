import logging
import sys

import requests
import time

from vkscriptz_core.errors import AccessError

logger = logging.getLogger('vk')


class VkApi(object):
    VERSION_ID = '5.40'

    def __init__(self, credentials):
        self.credentials = credentials

    def user_groups(self, user_id):
        for item in self._paginate(
            'https://api.vk.com/method/groups.get',
            1000,
            user_id=user_id,
            extended=1,
            fields='name,screen_name',
            access_token=self.credentials.access_token,
        ):
            yield item

    def _sleep(self, sec=0.4):
        logger.debug('sleep %s', sec)
        time.sleep(sec)

    def _paginate(self, url, count, **params):
        for offset in xrange(0, sys.maxint, count):
            if 'access_token' in params:
                self._sleep()
            data = self._get(url, **dict(params, offset=offset, count=count))
            try:
                items = data['response']['items']
            except:
                sys.stderr.write("no items in data: %s" % str(data))
                raise
            if not items:
                break
            for item in items:
                yield item

    def _get(self, url, **params):
        while True:
            logger.debug('get %s %s', url, params)
            resp = requests.get(url, params=dict(params, v=self.VERSION_ID))
            data = resp.json()
            if self._has_tmp_error(data):
                logger.warn('temporary error: %s', data['error'])
                self._sleep()
                continue
            break
        if self._has_access_error(data):
            logger.critical('access error: %s', data['error'])
            raise AccessError()
        return data

    def _has_tmp_error(self, data):
        return 'error' in data and data['error']['error_msg'].startswith((
            'Too many requests',
            'Internal server error',
        ))

    def _has_access_error(self, data):
        return 'error' in data and data['error']['error_msg'].startswith((
            'Access denied',
            'Access to group denied',
            'Permission to perform this action is denied',
        ))
