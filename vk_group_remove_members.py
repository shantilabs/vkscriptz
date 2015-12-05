#!/usr/bin/env python
from __future__ import unicode_literals

import sys, os

from _vkscriptz import vk_group_remove_member, vk_group_info, vk_info

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        sys.stderr.write('Please specify 1 group and at least 1 user\n')
        sys.exit(1)
    
    group_id = sys.argv[1]
    if not group_id.isdigit():
        gid = str(vk_group_info(group_id)['id'])
        sys.stderr.write('Group %s resolved to ID %s\n' % (group_id, gid))
        group_id = gid
        
    success, failed = (0, 0)
    for user_id in sys.argv[2:]:
        if not user_id.isdigit():
            info = list(vk_info(user_id))[0]
            user_id = str(info['id'])
        if vk_group_remove_member(group_id, user_id):
            success += 1
        else:
            failed += 1
    sys.stderr.write('Success: %d, failed %d\n' % (success, failed))
