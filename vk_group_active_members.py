#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import sys

from _vkscriptz import vk_wall, vk_wall_comments, vk_likes

if __name__ == '__main__':
    for owner_id in sys.argv[1:]:
        sys.stderr.write('group#{}\n'.format(owner_id))
        n = 0
        gid = '-' + owner_id
        for post in vk_wall(gid):
            for like in vk_likes(gid, 'post', post['id']):
                if like > 0:
                    print(like)
                    n += 1
            for comment in vk_wall_comments(gid, post['id']):
                if comment['from_id'] > 0:
                    print(comment['from_id'])
                    n += 1
                for like in vk_likes(gid, 'comment', comment['id']):
                    print(like)
                    n += 1
        sys.stderr.write('({} found)\n'.format(n))
