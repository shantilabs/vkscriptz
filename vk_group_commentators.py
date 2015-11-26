#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import sys

from _vkscriptz import vk_wall, vk_wall_comments


if __name__ == '__main__':
    for owner_id in sys.argv[1:]:
        sys.stderr.write('group#{}\n'.format(owner_id))
        n = 0
        for post in vk_wall('-' + owner_id):
            for comment in vk_wall_comments('-' + owner_id, post['id']):
                if comment['from_id'] > 0:
                    print(comment['from_id'])
                    n += 1
        sys.stderr.write('({} found)\n'.format(n))
