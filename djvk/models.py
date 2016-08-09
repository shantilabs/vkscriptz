# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models

from ..core.api import VkApi
from .helpers import DbCredentials, admincolumn


class Account(models.Model):
    updated = models.DateTimeField(auto_now=True)
    uid = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(blank=True, max_length=200, unique=True)
    first_name = models.CharField(blank=True, max_length=200)
    last_name = models.CharField(blank=True, max_length=200)
    groups = models.ManyToManyField('Group', blank=True, through='Subscription')

    def get_link(self):
        return VkApi.user_link(self.uid, self.screen_name) if self.uid else None

    def __unicode__(self):
        return self.name or self.get_link() or '(новый аккаунт)'

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'аккаунты'


class ManageredAccount(Account):
    access_token = models.CharField(max_length=255)
    is_default = models.BooleanField('', default=False)

    def has_access_token(self):
        return bool(self.access_token)

    @classmethod
    def get_default(cls):
        return cls.objects.filter(is_default=True).first()

    def get_vk_api(self):
        return VkApi(DbCredentials(self))

    def update(self):
        api = self.get_vk_api()
        fields = (
            'first_name',
            'last_name',
            'screen_name',
        )
        info = api.self_info(fields)
        for k in fields:
            setattr(self, k, info['k'])
        self.uid = info['id']
        for data in api.user_groups((
            'name',
            'screen_name'
            'type',
        )):
            group, _created = Group.objects.update_or_create(
                gid=data['id'],
                defaults=dict(
                    name=data['name'],
                    screen_name=data['screen_name'],
                    type=Group.from_vk_type(data['type']),
                )
            )
            Subscription.objects.update_or_create(
                account=self,
                group=group,
                defaults=dict(
                    is_admin=data['is_admin'],
                    is_member=data['is_member'],
                ),
            )

    def save(self, *args, **kwargs):
        if self.access_token:
            self.update()
        other_defaults = ManageredAccount.objects.filter(is_default=True)
        if not other_defaults.exists():
            self.is_default = True
        elif self.pk and self.is_default and other_defaults.exists():
            other_defaults.update(is_default=False)
        super(ManageredAccount, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'управляемый аккаунт'
        verbose_name_plural = 'управляемые аккаунты'


class Group(models.Model):
    updated = models.DateTimeField(auto_now=True)
    gid = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(blank=True, max_length=200, unique=True)
    name = models.CharField(u'название', blank=True, max_length=200)

    TYPE_GROUP = 1
    TYPE_PAGE = 2
    TYPE_EVENT = 3
    TYPE_CHOICES = (
        (TYPE_GROUP, 'группа'),
        (TYPE_PAGE, 'публичная страница'),
        (TYPE_EVENT, 'мероприятие'),
    )
    _vk_types = {
        'group': TYPE_GROUP,
        'page': TYPE_PAGE,
        'event': TYPE_EVENT,
    }
    type = models.SmallIntegerField(choices=TYPE_CHOICES)

    def to_vk_type(self):
        return {v: k for k,v in self._vk_types.items()}

    @classmethod
    def from_vk_type(cls, k):
        return cls._vk_types[k]

    @admincolumn('тип')
    def type_description(self):
        return dict(self.TYPE_CHOICES)[self.type]

    def get_link(self):
        return VkApi.group_link(
            self.gid,
            self.to_vk_type(),
            self.screen_name,
        ) if self.gid else None

    @admincolumn('админ')
    def get_default_admin(self):
        return self.subscriptions.filter(is_admin=True).first().account

    def __unicode__(self):
        return self.name or self.get_link() or '(новая группа)'

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'


class Subscription(models.Model):
    group = models.ForeignKey(Group, related_name='subscriptions')
    account = models.ForeignKey(Account)
    updated = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)

    ADMIN_LEVEL_MODER = 1
    ADMIN_LEVEL_EDITOR = 2
    ADMIN_LEVEL_ADMIN = 3
    ADMIN_LEVEL_CHOICES = (
        (ADMIN_LEVEL_MODER, 'модератор'),
        (ADMIN_LEVEL_EDITOR, 'редактор'),
        (ADMIN_LEVEL_ADMIN, 'админ'),
    )
    admin_level = models.SmallIntegerField(null=True)

    @admincolumn('роль')
    def admin_level_description(self):
        return dict(self.ADMIN_LEVEL_CHOICES)[self.admin_level]

    class Meta:
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'
