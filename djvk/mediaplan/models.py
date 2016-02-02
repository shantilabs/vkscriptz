# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.db.models import Q
from django.utils import timezone

from ..models import Group


class Tag(models.Model):
    name = models.CharField(
        'тэг',
        max_length=50,
        unique=True,
        help_text='например: «демотиватор», «статья», «фото котиков»',
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'тэг (для редакции)'
        verbose_name_plural = 'тэги (для редакции)'
        ordering = (
            'name',
        )


def default_rule_min_pub_time():
    rule = MediaplanRule.objects.last()
    return rule.min_pub_time if rule else datetime.time(13)


def default_rule_max_pub_time():
    rule = MediaplanRule.objects.last()
    return rule.min_pub_time if rule else datetime.time(22)


def default_rule_group():
    rule = MediaplanRule.objects.last()
    return rule.group if rule else None


class MediaplanRule(models.Model):
    group = models.ForeignKey(
        Group,
        default=default_rule_group,
        verbose_name='группа',
        limit_choices_to=Q(
            subscriptions__is_admin=True,
        ),
    )
    tag = models.ForeignKey(
        Tag,
        related_name='rules',
        verbose_name='тэг',
    )
    min_pub_time = models.TimeField(
        'время публикации от',
        default=default_rule_min_pub_time,
    )
    max_pub_time = models.TimeField(
        'время публикации до',
        default=default_rule_max_pub_time,
    )
    min_interval_hours = models.IntegerField(
        verbose_name='частота публикаций этого тэга',
        default=24,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'правило медиаплана'
        verbose_name_plural = 'правила медиаплана'
        unique_together = (
            ('group', 'tag'),
        )


def default_post_group():
    post = DelayedPost.objects.first()
    return post.group if post else None


class DelayedPost(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    post_id = models.BigIntegerField(editable=False, null=True)
    published = models.DateTimeField(null=True)
    group = models.ForeignKey(Group, default=default_post_group)
    text = models.TextField('текст')
    desired_datetime = models.DateTimeField('желаемое время', null=True,
                                            help_text='если надо')
    tags = models.ManyToManyField(Tag, verbose_name='тэги',
                                  related_name='posts')

    def age_hours(self):
        if not self.published:
            return None
        return (timezone.now() - self.published).total_seconds() / 3600

    @classmethod
    def get_next(cls):
        now = timezone.now()
        concrete_post = cls.objects.filter(
            desired_datetime__gte=now,
            post_id=None,
        ).order_by(
            'id',
        ).first()
        if concrete_post:
            return concrete_post
        for tag in Tag.objects.filter(
            rules__min_pub_time__lte=now.time(),
            rules__max_pub_time__gte=now.time(),
        ).order_by('?'):
            last_post = tag.posts.exclude(
                published=None,
            ).order_by(
                'published',
            ).last()
            if not last_post or last_post.age_hours() >= tag.min_interval_hours:
                return tag.posts.all().order_by('?').first()

    def save(self, *args, **kwargs):
        if self.post_id:
            self.published = timezone.now()
        super(DelayedPost, self).save()

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = (
            '-created',
        )


class DelayedPostImage(models.Model):
    delayed_post = models.ForeignKey(DelayedPost)
    image = models.ImageField(upload_to='posts')
    description = models.TextField('текст', blank=True,
                                   help_text='(если надо)')

    class Meta:
        verbose_name = 'картинка'
        verbose_name_plural = 'картинки'
        ordering = (
            'id',
        )
