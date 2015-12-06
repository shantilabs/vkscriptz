#!/bin/bash
set -e
./vk.py user_groups `./vk.py group_members $1` | cut -f2 | sort | uniq -c | sort -nr | head -n 120
