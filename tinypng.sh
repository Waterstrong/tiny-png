#!/bin/sh

CHANGES_TAG="Changes"
CURRENT_DIR=$(dirname "$(readlink "$0")")

upgrade_script() {
    if git -C "${CURRENT_DIR}" status | grep -iq "${CHANGES_TAG}"; then
        echo 'The script contains uncommitted changes. Do you want to discard them? Choose the number:'
        options=("Yes - Override the changes!" "No  - Keep my local changes!")
        select yn in "${options[@]}"; do
            case $yn in
                "${options[0]}" )
                git -C "${CURRENT_DIR}" reset --hard >/dev/null 2>&1 &
                break;;
                "${options[1]}" ) break;;
            esac
        done
    fi

    git -C "${CURRENT_DIR}" pull -r >/dev/null 2>&1 &
}

upgrade_script
python "${CURRENT_DIR}/compress.py" $1