#!/bin/bash
set -e
./vk_user_groups.py `./vk_group_members.py $1` | cut -f2 | sort | uniq -c | sort -nr | head -n 120
