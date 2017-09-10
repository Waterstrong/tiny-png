#!/bin/sh

argv=$1
current_dir=$(dirname "$(readlink "$0")")
git -C "${current_dir}" pull -f
python "${current_dir}/compress.py" ${argv}