#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import sys

from _vkscriptz import vk_instagrams


if __name__ == '__main__':
    for group_id in sys.argv[1:]:
        for account in vk_instagrams(group_id):
            print('https://www.instagram.com/{account}/'.format(
                account=account,
            ))
