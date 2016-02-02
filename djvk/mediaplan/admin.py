# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.DelayedPost)
class DelayedPostAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'published',
        'group',
        'text',
        'desired_datetime',
    )
    list_filter = (
        'tags',
        'group',
    )


@admin.register(models.MediaplanRule)
class MediaplanRuleAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'tag',
        'min_pub_time',
        'max_pub_time',
        'min_interval_hours',
    )
    list_display_links = (
        'group',
        'tag',
    )
