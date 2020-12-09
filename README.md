# Theia

Automating aspects of image generation

## Python

The scripts in this repository are designed to work with Python 3.90, utilising the new type hinting features in this version of Python. I strongly recommend using Python 3.90 or newer when running these scripts.

All scripts are designed to be executed from the root directory, eg:
`python ./python/generate_letter_set.py output`

### Formatting

Formatting is done with [Black](https://github.com/psf/black).

### Tests

Testing is done with the standard `unittest` library. To run tests from the root directory:

```
cd python
python -m unittest
```

## Blender

Some of the scripts in this repository interface with Blender to generate 3D models. In order for these scripts to work easily, you will need to ensure that Blender is added to PATH.

Some scripts may use the following plugins:

- [Blender Source Tools](https://github.com/Artfunkel/BlenderSourceTools)
- [VHAC-D](https://github.com/andyp123/blender_vhacd)

These addons have been tested to work with Blender 2.83. At the time of writing, these addons do not work with Blender 2.9+, however there are workarounds for this if you're inclined to deal with that.
