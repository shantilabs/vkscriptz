#!/bin/bash
set -e
./vk_user_groups.py `./vk_group_members.py $1` | cut -f2 | sort | uniq -c | sort -dr | head -n 120
