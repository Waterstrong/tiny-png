import os
import sys
import re
import tinify

tinify_key_file = open('tinify.key', 'r')
tinify.key = tinify_key_file.read()
tinify_key_file.close()

# TODO: support more image types?
image_pattern = re.compile('.*\.(jpg$|png$)')


def Scanning(rootDir):
    for file in os.listdir(rootDir):
        path = os.path.join(rootDir, file)
        if os.path.isdir(path):
            Scanning(path)
        elif image_pattern.match(path):
            print 'Start to compress image:', path
            tinify.from_file(path).to_file(path)
            print 'Compression done!\n'


if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
    # TODO: check y or n after input
    Scanning(sys.argv[1])
    if tinify.compression_count is not None:
        print 'You have already used', tinify.compression_count, 'number of compressions this month.'
    else:
        print '**Warning:**\n   Nothing to compress in directory:', sys.argv[1]
else:
    print 'Usage: python', sys.argv[0], '<target_directory>'


