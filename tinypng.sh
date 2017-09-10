#!/bin/sh

argv=$1
current_dir=$(dirname "$(readlink "$0")")

upgrade_script() {
    git -C "${current_dir}" pull -r
    echo ''
}

case ${argv} in
    upgrade) upgrade_script;;
    *) python "${current_dir}/compress.py" ${argv};;
esac