import os
import sys
import re
import tinify

# TODO: support more image types?
image_pattern = re.compile('.*\.(jpg$|png$)')

def initializeTinifyKey():
    print 'Initializing tinify key...'
    tinify_key_file = open('tinify.key', 'r')
    tinify.key = tinify_key_file.read()
    tinify_key_file.close()


def scanning(rootDir):
    for file in os.listdir(rootDir):
        path = os.path.join(rootDir, file)
        if os.path.isdir(path):
            scanning(path)
        elif image_pattern.match(path):
            print 'Start compressing image:', path
            tinify.from_file(path).to_file(path)
            print 'Compression done!\n'


def showCompressCount():
    if tinify.compression_count is not None:
        print 'You have already used', tinify.compression_count, 'number of compressions this month.'
    else:
        print '**Warning:**\n   Nothing to compress in directory:', sys.argv[1]


def confirmCompression(path):
    input = raw_input('Are you sure to compress all images under:\n  {}\n(y or n ?): '.format(path))
    if input != 'y':
        print 'Compression aborted!'
        sys.exit()


if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
    confirmCompression(sys.argv[1])
    initializeTinifyKey()
    scanning(sys.argv[1])
    showCompressCount()
else:
    print 'Usage: python', sys.argv[0], '<target_directory>'


# TODO: resizing width and height?