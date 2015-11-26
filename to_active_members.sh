#!/bin/bash
set -e
for f in `find $1 -type f`; do
    dest=active_members/$f
    echo "$f => $dest"
    mkdir -p `dirname $dest`
    ./vk_group_active_members.py `cat $f | cut -f1` | sort | uniq > $dest
done
