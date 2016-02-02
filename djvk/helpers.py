# -*- coding: utf-8 -*-
from django.conf import settings


class DbCredentials(object):
    client_id = settings.DJVK_CLIENT_ID
    client_secret = settings.DJVK_CLIENT_SECRET
    access_token = None

    def __init__(self, account):
        self._account = account

    def load(self):
        pass

    def save(self):
        self._account.access_token = self.access_token
        self._account.save()


def admincolumn(
    short_description=None,
    allow_tags=False,
    sort_as=None,
    boolean=False,
):
    def decorator(func):
        if short_description:
            func.short_description = short_description
        if allow_tags:
            func.allow_tags = allow_tags
        if sort_as:
            func.admin_order_field = sort_as
        if boolean:
            func.boolean = True
        return func
    return decorator
