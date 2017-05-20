import os
import re
import sys
import tinify
from PIL import Image

ENABLE_RECURSIVELY_SCAN = True

ENABLE_RESIZING = False
MAX_HEIGHT = 1200
RESIZE_HEIGHT = 1000

FREE_NUMBER_MONTHLY = 500
TINIFY_KEY_FILE = 'tinify.key'
TINIFY_CACHE_FILE = '.tinify.cache'
IMAGE_PATTERN = re.compile('.*\.(jpg$|jpeg$|png$)', re.I)


def load_tinify_key():
    print 'Initializing tinify key...\n'
    with open(TINIFY_KEY_FILE, 'r') as file:
        tinify.key = file.read()


def compress_images(root_dir, recursively):
    tinified_cache = load_tinified_cache(root_dir)
    for file in os.listdir(root_dir):
        path = os.path.join(root_dir, file)
        if os.path.isdir(path):
            if recursively:
                compress_images(path, recursively)
            else:
                print 'Subdirectory scanning ignored:', path
        elif IMAGE_PATTERN.match(path):
            tinify_image(path, tinified_cache)


def tinify_image(path, tinified_cache):
    print 'Start compressing image:', path
    if (path + '\n') not in tinified_cache:
        with Image.open(path) as image:
            (width, height) = image.size
            if ENABLE_RESIZING and height > MAX_HEIGHT and width > MAX_HEIGHT:
                tinify.from_file(path).resize(method="scale", height=RESIZE_HEIGHT).to_file(path)
            else:
                tinify.from_file(path).to_file(path)
        with open(get_cache_file(path), 'a') as file:
            file.write(path + '\n')
            print 'Compression done!\n'
    else:
        print 'Compression ignored. Found record in \'{}\'.\n'.format(TINIFY_CACHE_FILE)


def load_tinified_cache(path):
    cache_path = get_cache_file(path)
    if not os.path.exists(cache_path):
        return []
    with open(cache_path, 'r') as file:
        return file.readlines()


def get_cache_file(path):
    parent_path = os.path.isdir(path) and path or os.path.dirname(path)
    return os.path.join(parent_path, TINIFY_CACHE_FILE)


def show_compressed_count():
    if tinify.compression_count is not None:
        print 'You have already used {}/{} free number of compressions this month.\n'.format(tinify.compression_count, FREE_NUMBER_MONTHLY)
    else:
        print '**Warning:**\n   Nothing to compress in the directory.'


def confirm_compression(path):
    input = raw_input('Are you sure to compress all images under:\n  {}\n(y or n ?): '.format(path))
    if input != 'y':
        print 'Compression aborted!'
        sys.exit()


def output_help():
    print 'The script will compress all case insensitive \'*.jpg|*.jpeg|*.png\' target image or images in target directory recursively'
    print 'Usage:\n  python', sys.argv[0], '<target_image>\n', '  python', sys.argv[0], '<target_directory>\n'
    print 'GitHub: https://github.com/waterstrong/tiny-png'


if len(sys.argv) == 2:
    input_path = sys.argv[1]
    if os.path.isdir(input_path):
        load_tinify_key()
        confirm_compression(input_path)
        compress_images(input_path, ENABLE_RECURSIVELY_SCAN)
        show_compressed_count()
    elif IMAGE_PATTERN.match(input_path):
        load_tinify_key()
        tinify_image(input_path, load_tinified_cache(input_path))
        show_compressed_count()
    else:
        output_help()
else:
    output_help()
