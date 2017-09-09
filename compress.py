import os
from os.path import realpath
import re
import sys
import timeit
import tinify
from PIL import Image
from datetime import datetime

ENABLE_RECURSIVELY_SCAN = True

ENABLE_RESIZING = True
MAX_HEIGHT = 1366
RESIZE_HEIGHT = 1080

FREE_NUMBER_MONTHLY = 500
SCRIPT_DIR = os.path.split(realpath(__file__))[0]
TINIFY_KEY_FILE = os.path.join(SCRIPT_DIR, 'tinify.key')
TINIFY_LOG_FILE = os.path.join(SCRIPT_DIR, 'tinify.log')
TINIFY_CACHE_FILE = '.tinify.cache'
IMAGE_PATTERN = re.compile('.*\.(jpg$|jpeg$|png$)', re.I)
COMMAND = 'tinypng'

def scan_target_images(root_dir, recursively):
    write_log('Scanning directory: {}'.format(realpath(root_dir)))
    tinified_cache = load_tinified_cache(root_dir)
    target_images = []
    for file in os.listdir(root_dir):
        path = os.path.join(root_dir, file)
        if os.path.isdir(path):
            if recursively:
                target_images.extend(scan_target_images(path, recursively))
            else:
                print '> Subdirectory scanning ignored: {}'.format(realpath(path))
        elif IMAGE_PATTERN.match(path):
            if get_cache_key(file) not in tinified_cache:
                target_images.append(path)
                write_log('Scanned image: {}'.format(realpath(path)))
            else:
                print '> Image ignored: {}. Found record in \'{}\'.'.format(realpath(path), TINIFY_CACHE_FILE)
    image_number = len(target_images)
    write_log('Found {} target {} in directory \'{}\'\n'.format(image_number, image_number > 1 and 'images' or 'image', realpath(root_dir)))
    return target_images


def load_tinify_key():
    write_log('Initializing tinify key...\n')
    with open(TINIFY_KEY_FILE, 'r') as file:
        tinify.key = file.read()


def compress_directory_images(input_path):
    target_images = scan_target_images(input_path, ENABLE_RECURSIVELY_SCAN)
    confirm_compression(input_path, len(target_images))
    compress_images(target_images)
    show_compressed_count()


def compress_target_image(input_path):
    load_tinify_key()
    if get_cache_key(input_path) not in load_tinified_cache(input_path):
        compress_images([input_path])
        show_compressed_count()
    else:
        write_log('Start compressing image: {}'.format(realpath(input_path)))
        write_log('Compression ignored (1/1). Found record in \'{}\'.\n'.format(TINIFY_CACHE_FILE))


def compress_images(target_images):
    current = 0
    total_number = len(target_images)
    total_time = 0
    for image_file in target_images:
        current += 1
        write_log('Start compressing image: {}'.format(realpath(image_file)))
        if os.path.exists(image_file):
            time_start = timeit.default_timer()
            tinify_image(image_file)
            time_diff = round(timeit.default_timer() - time_start, 2)
            total_time += time_diff
            write_log('Compression done takes {} seconds! ({}/{})\n'.format(time_diff, current, total_number))
        else:
            write_log('Ignored: target image does not exist! ({}/{})\n'.format(current, total_number))
    if total_time > 0:
        write_log('Totally takes {} seconds to complete!'.format(total_time))


def tinify_image(image_file):
    with Image.open(image_file) as image:
        (width, height) = image.size
        write_log('  - Compressing... Original image dimensions: {} x {}'.format(width, height))
        if ENABLE_RESIZING and height > MAX_HEIGHT and width > MAX_HEIGHT:
            scaled_width = width * RESIZE_HEIGHT / height
            write_log('  - Exceed max {} x {}. Scaling to new dimensions: {} x {}'.format(MAX_HEIGHT, MAX_HEIGHT, scaled_width, RESIZE_HEIGHT))
            tinify.from_file(image_file).resize(method="scale", height=RESIZE_HEIGHT).to_file(image_file)
        else:
            tinify.from_file(image_file).to_file(image_file)
    with open(get_cache_file(image_file), 'a') as file:
        file.write(get_cache_key(image_file))


def load_tinified_cache(path):
    cache_path = get_cache_file(path)
    if not os.path.exists(cache_path):
        return []
    with open(cache_path, 'r') as file:
        return file.readlines()


def get_cache_key(path):
    return os.path.basename(path) + '\n'


def get_cache_file(image_path):
    parent_path = os.path.isdir(image_path) and image_path or os.path.dirname(image_path)
    return os.path.join(parent_path, TINIFY_CACHE_FILE)


def show_compressed_count():
    if tinify.compression_count is not None:
        write_log('You have already used {}/{} free number of compressions this month.\n'.format(tinify.compression_count, FREE_NUMBER_MONTHLY))
    else:
        write_log('**Warning**: Nothing to compress in the directory!\n')


def confirm_compression(path, number):
    if number > 0:
        input = raw_input('Are you sure to compress all {} images under:\n    {}\n(y or n ?): '.format(number, realpath(path)))
        if input == 'y':
            load_tinify_key()
        else:
            write_log('Compression aborted with confirmation!\n')
            sys.exit()


def write_log(message):
    print '>', message
    with open(TINIFY_LOG_FILE, 'a') as file:
        file.write('> {} {}\n'.format(datetime.now(), message))


def output_help():
    print '\nThe TinyPNG script can compress all case insensitive \'*.jpg|*.jpeg|*.png\' target image or images in target directory recursively.'
    print '\nUsage:'
    print '  ', COMMAND, ' <target_image>'
    print '  ', COMMAND, ' <target_directory>'
    print '\nGitHub Repo: https://github.com/waterstrong/tiny-png\n'

def main():
    if len(sys.argv) == 2:
        input_path = sys.argv[1]
        if os.path.isdir(input_path):
            compress_directory_images(input_path)
        elif IMAGE_PATTERN.match(input_path) and os.path.exists(input_path):
            compress_target_image(input_path)
        else:
            output_help()
    else:
        output_help()


main()