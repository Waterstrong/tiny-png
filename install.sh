#!/bin/sh

SYMBOL_LINK=/usr/local/bin/tinypng
TINY_PNG_FILE=${PWD}/tinypng.sh
TINIFY_KEY_FILE=tinify.key
TINIFY_PAGE=https://tinypng.com/dashboard/developers

add_tiny_png_symbol_link() {
    echo "> Adding symbol link '${SYMBOL_LINK} -> ${TINY_PNG_FILE}'..."
    ln -sf "${TINY_PNG_FILE}" "${SYMBOL_LINK}"
}


edit_tinify_key_file() {
    echo '\nDid you get your Tinify API Key before? Choose the number:'
    options=("Yes - I've already configured the Tinify API Key!" "No  - I don't know what the Tinify API Key is!")
    select yn in "${options[@]}"; do
        case $yn in
            "${options[0]}" )
            break;;
            "${options[1]}" )
            if [ ! -e ${TINIFY_KEY_FILE} ]; then
                cp ${TINIFY_KEY_FILE}.template ${TINIFY_KEY_FILE}
            fi
            open ${TINIFY_PAGE}
            echo ''
            read -p "Once you copied your Tinify API Key, press any key to continue edit ${TINIFY_KEY_FILE} file..."
            vim ${TINIFY_KEY_FILE}
            break;;
        esac
    done
    echo ''
}

main() {
    pip install --upgrade tinify
    pip install image
    add_tiny_png_symbol_link
    edit_tinify_key_file
    echo "> Tiny PNG installed. Type 'tinypng help' for more details. Enjoy!\n"
}

main
