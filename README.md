# Theia

Automating aspects of image generation

## Python

The scripts in this repository are designed to work with Python 3.90, utilising the new type hinting features in this version of Python. I strongly recommend using Python 3.90 or newer when running these scripts. I've created a .python-version file so, if all goes well, pyenv should help out with this.

All scripts are designed to be executed from the root directory. I recommend executing as a module, eg:
`python -m theia.projects.generate_letter_set.py`

### Formatting

Formatting is done with [Black](https://github.com/psf/black).

### Tests

Testing is done with the standard `unittest` library. To run tests from the root directory:

```
python -m unittest
```

## VTFCmd

Some of the scripts in this repository use VTFCmd to convert textures into the .vtf file format required by Source Engine games. To install this, run `./scripts/install_vtfcmd.sh`

## Blender

Some of the scripts in this repository interface with Blender to generate 3D models. In order for these scripts to work easily, you will need to ensure that Blender is added to PATH.

These scripts are built and tested on Blender 2.91. Some of these scripts may use the following plugins:

- [Blender Source Tools](https://github.com/Artfunkel/BlenderSourceTools)
- [VHAC-D](https://github.com/tpdickso/blender_vhacd)

At the time of writing, these addons are not well supported for Blender 2.9+ so you will need to set these up manually.
