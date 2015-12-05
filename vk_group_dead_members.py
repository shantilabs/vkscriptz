#!/usr/bin/env python
from __future__ import unicode_literals

import sys, os

from _vkscriptz import vk_group_members, vk_info, format_dict, coding


if __name__ == '__main__':
    for group_id in sys.argv[1:]:
        sys.stderr.write('group %s: ' % group_id)
        dead_n = 0
        users = list(vk_group_members(
            group_id,
            city_id=os.environ.get('CITY_ID'),
        ))
        sys.stderr.write(' (%d users) ' % len(users))
        for info in vk_info(users):
            if "deactivated" in info:
                print info['id']
                dead_n += 1
        sys.stderr.write("- %s dead\n" % dead_n)
