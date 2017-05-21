# tiny-png
To compress and optimize JPEG and PNG images with [Tinify API in Python](https://tinypng.com/developers/reference/python).

## Installation
```
pip install --upgrade tinify
pip install image

git clone https://github.com/Waterstrong/tiny-png.git

cd tiny-png
```

## Usage

- After clone `tiny-png`, change `tinify.key.template` to `tinify.key`
- Paste your **tinify key** in it. Then start to compress the images in `target_directory` recursively
```
python compress.py <target_image>
python compress.py <target_directory>
```

Checkout the cache file `.tinify.cache` in each target directory. It can prevent duplicated compression.

Checkout the log file `tinify.log` in current `compress.py` execution directory for compression details.

**IMPORTANT:** The script will compress all case insensitive `*.jpg|*.jpeg|*.png` target image or images in target directory recursively.

## Results
#### Before Compression
![Before Compression](img/before_compress.png)

#### After Compression:
![After Compression](img/after_compress.png)

## Powered By:
- [https://tinypng.com/](https://tinypng.com/)