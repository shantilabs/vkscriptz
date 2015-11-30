#!/bin/bash
set -e
./vk_user_groups.py  | cut -f2 | sort | uniq -c | sort -dr | head -n 100
