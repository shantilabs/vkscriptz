#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import sys

from _vkscriptz import vk_user_groups, coding

if __name__ == '__main__':
    for user_id in sys.argv[1:]:
        for item in vk_user_groups(user_id):
            print(
                '{item[id]}\thttps://vk.com/{item[screen_name]}\t{item[name]}'.
                    format(item=item).encode(coding),
            )
