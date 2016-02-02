# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import urllib

from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect

from core.api import VkApi
from . import models
from .helpers import admincolumn, DbCredentials


@admin.register(models.ManageredAccount)
class ManageredAccountAdmin(admin.ModelAdmin):
    list_display = (
        'uid',
        'updated',
        'first_name',
        'last_name',
        'link',
        'is_default',
        'has_access_token',
    )
    list_display_links = (
        'updated',
        'first_name',
        'last_name',
    )
    readonly_fields = list_display + (
        'groups',
    )

    def vkauth(self, request):
        return HttpResponse('123')

    def get_urls(self):
        return [
            url('vkauth', self.vkauth, name='vkauth'),
        ] + super(ManageredAccountAdmin, self).get_urls()

    @admincolumn('ссылка', allow_tags=True)
    def link(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.get_link())

    def add_view(self, request, form_url='', extra_context=None):
        return redirect('https://oauth.vk.com/authorize?' + urllib.urlencode(dict(
            client_id=DbCredentials.client_id,
            redirect_uri=request.build_absolute_uri(reverse('admin:vkauth')),
            display='page',
            scope=','.join((
                'offline',
                'groups',
            )),
            # response_type='code',
            response_type='token',
            v=VkApi.VERSION_ID,
        )))


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'gid',
        'updated',
        'name',
        'link',
        'type_description',
        'get_default_admin',
    )
    readonly_fields = list_display

    @admincolumn('ссылка', allow_tags=True)
    def link(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.get_link())

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
