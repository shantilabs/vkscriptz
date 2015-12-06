#!/bin/bash
set -e
./vk.py user_groups  | cut -f2 | sort | uniq -c | sort -nr | head -n 100
