#!/usr/bin/env python
from __future__ import unicode_literals

import sys, os

from _vkscriptz import vk_group_remove_member

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        sys.stderr.write('Please specify 1 group and t least 1 user\n')
        sys.exit(1)
    
    group_id = sys.argv[1]
    success, failed = (0, 0)
    for user_id in sys.argv[2:]:
        if vk_group_remove_member(group_id, user_id):
            success += 1
        else:
            failed += 1
    sys.stderr.write('Success: %d, failed %d\n' % (success, failed))
