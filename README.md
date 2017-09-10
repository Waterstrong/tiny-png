# tiny-png
To compress and optimize JPEG and PNG images with [Tinify API in Python](https://tinypng.com/developers/reference/python).

## Installation and Setup (Mac OS supported only)

1. Clone the project: `git clone https://github.com/Waterstrong/tiny-png.git` 

2. Execute the `install.sh` script and follow the instructions to complete the whole process

3. Pay attention to the Tinify Key in `tinify.key`


## Usage

The TinyPNG script can compress all case insensitive `*.jpg|*.jpeg|*.png` target image or images in target directory recursively.
```
Usage:
   tinypng  help
   tinypng  <target_image>
   tinypng  <target_directory>
```

Checkout the cache file `.tinify.cache` in each target directory. It can prevent duplicated compression.

Checkout the log file `<your_dir>/tiny-png/tinify.log` for compression details log.

**IMPORTANT:** The script will compress all case insensitive `*.jpg|*.jpeg|*.png` target image or images in target directory recursively.

## Results
#### Before Compression
![Before Compression](img/before_compress.png)

#### After Compression:
![After Compression](img/after_compress.png)

## Powered By:
- [https://tinypng.com/](https://tinypng.com/)