# tiny-png
To compress and optimize JPEG and PNG images with [Tinify API in Python](https://tinypng.com/developers/reference/python).

## Installation
```
pip install --upgrade tinify

git clone https://github.com/Waterstrong/tiny-png.git

cd tiny-png
```

## Usage

- After clone `tiny-png`, change `tinify.key.template` to `tinify.key`
- Paste your **tinify key** in it. Then start to compress the images in `target_directory`
```
python compress.py <target_directory>
```

**IMPORTANT:** The script will replace all the `*.jpg|*.png` images in the target directory.

## Powered By:
- [https://tinypng.com/](https://tinypng.com/)