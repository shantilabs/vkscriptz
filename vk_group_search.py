#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import sys

from _vkscriptz import vk_group_search, coding

if __name__ == '__main__':
    for q in sys.argv[1:]:
        for item in vk_group_search(
            q.decode(coding),
            sort=2,
            country_id=1,
        ):
            print(
                '{item[id]}\t{item[name]}'.format(item=item).encode(coding),
            )
