#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import os
import sys
from collections import defaultdict

from _vkscriptz import vk_group_members, vk_are_members, format_dict, coding


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        sys.stderr.write('Please specify at least 2 groups\n')
        sys.exit(1)
    
    users = list(vk_group_members(
        sys.argv[1],
        city_id=os.environ.get('CITY_ID'),
    ))
    matched = defaultdict(lambda: 0)
    
    sys.stderr.write('checking %d users for %d other groups\n' % (len(users), len(sys.argv)-2))
    for group_id in sys.argv[2:]:
        members = [item['user_id'] for item in vk_are_members(group_id, users) if item['member'] == 1]
        for m in members:
            matched[str(m)] += 1
    
    sys.stderr.write('%d member(s)\n' % len(matched))
    for u, c in matched.iteritems():
        print("%s %d" % (u, c))
