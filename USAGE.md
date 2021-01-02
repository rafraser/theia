# Usage

Here's a quick crash course on getting things running. This repo has a wide range of scripts, so I'd recommend only installing what you need to start with.

My personal dev environment uses Windows 10 with Git Bash. Your mileage may vary with different environments.

## Python

The scripts in this repository are designed to work with Python 3.90. A .python-version file is included in the repo for use with pyenv.

### Running Projects

All projects are designed to be run as modules from the root directory, eg:

```bash
python -m theia.projects.palette_apply -h
```

### Formatting

Formatting is done with [Black](https://github.com/psf/black).

### Tests

Testing is done with the standard **unittest** library. To run tests from the root directory: `python -m unittest`

## Additional Tools

Some of the scripts in this repository work with additional tools for texture conversion, 3D modelling, etc.

### VTFCmd

Some scripts use VTFCmd to convert textures into the .vtf file format required by Source Engine games. VTFCmd.exe should be installed into the root directory. You can install this by running `./scripts/install_vtfcmd.sh`

### Blender

Some scripts interface with Blender to generate 3D models, or take advantage of Blender's procedural texturing. In order for these scripts to function, you will need to ensure that Blender is added to PATH.

These scripts are built and tested on **Blender 2.91**. They may not work on older versions of Blender.

Some scripts may use the following plugins:

- [Blender Source Tools](https://github.com/Artfunkel/BlenderSourceTools)
- [VHAC-D](https://github.com/tpdickso/blender_vhacd)

At the time of writing, the "main" releases of these plugins are not designed for Blender 2.9+, so you will need to look around carefully to ensure compatibility. Sorry.
