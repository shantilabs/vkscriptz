#!/bin/bash
set -e
./vk_user_groups.py  | cut -f2 | sort | uniq -c | sort -nr | head -n 100
