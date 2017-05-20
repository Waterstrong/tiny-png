import os
import sys
import re
import tinify

IMAGE_PATTERN = re.compile('.*\.(jpg$|jpeg$|png$)', re.I)

def load_tinify_key(key_file):
    print 'Initializing tinify key...'
    tinify_key_file = open(key_file, 'r')
    tinify.key = tinify_key_file.read()
    tinify_key_file.close()


def compress_images(root_dir, recursively):
    for file in os.listdir(root_dir):
        path = os.path.join(root_dir, file)
        if os.path.isdir(path):
            if recursively:
                compress_images(path, recursively)
            else:
                print 'Subdirectory scanning ignored:', path
        elif IMAGE_PATTERN.match(path):
            print 'Start compressing image:', path
            # tinify.from_file(path).to_file(path)
            print 'Compression done!\n'


def show_compressed_count():
    if tinify.compression_count is not None:
        print 'You have already used', tinify.compression_count, 'number of compressions this month.'
    else:
        print '**Warning:**\n   Nothing to compress in the directory.'


def confirm_compression(path):
    input = raw_input('Are you sure to compress all images under:\n  {}\n(y or n ?): '.format(path))
    if input != 'y':
        print 'Compression aborted!'
        sys.exit()


if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
    confirm_compression(sys.argv[1])
    load_tinify_key('tinify.key')
    compress_images(sys.argv[1], True)
    show_compressed_count()
else:
    print 'Usage: python', sys.argv[0], '<target_directory>'


# TODO: resizing width and height?