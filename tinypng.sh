#!/bin/sh

argv=$1
current_dir=$(dirname "$(readlink "$0")")
git -C "${current_dir}" reset --hard >/dev/null 2>&1 &
git -C "${current_dir}" pull -r >/dev/null 2>&1 &
python "${current_dir}/compress.py" ${argv}