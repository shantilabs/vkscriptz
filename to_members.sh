#!/bin/bash
set -e
for f in `find $1 -type f`; do
    dest=members/$f
    echo "$f => $dest"
    mkdir -p `dirname $dest`
    ./vk.py group_members `cat $f | cut -f1` | sort | uniq > $dest
done
