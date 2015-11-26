#!/bin/bash
set -e
for f in `find $1 -type f`; do
    dest=commentators/$f
    echo "$f => $dest"
    mkdir -p `dirname $dest`
    ./vk_group_commentators.py `cat $f | cut -f1` | sort | uniq > $dest
done
