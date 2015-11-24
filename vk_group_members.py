#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import sys

from _vkscriptz import vk_group_members, format_dict, coding

if __name__ == '__main__':
    fields = [
        'city',
        'online',
    ]
    for group_id in sys.argv[1:]:
        for user in vk_group_members(group_id, fields=fields):
            if isinstance(user, dict):
                print(format_dict(user).encode(coding))
            else:
                print(user)
