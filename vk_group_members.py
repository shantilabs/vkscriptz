#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import os
import sys

from _vkscriptz import vk_group_members, format_dict, coding


if __name__ == '__main__':
    for group_id in sys.argv[1:]:
        sys.stderr.write('group#{}\n'.format(group_id))
        n = 0
        for user in vk_group_members(
            group_id,
            city_id=os.environ.get('CITY_ID'),
        ):
            if isinstance(user, dict):
                print(format_dict(user).encode(coding))
            else:
                print(user)
            n += 1
        sys.stderr.write('({} member(s))\n'.format(n))
