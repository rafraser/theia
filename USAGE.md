# Usage

## Getting Started

### Installation

You'll need Python for these scripts - these scripts are developed with Python 3.9, but may work on older versions. If you're using pyenv, a .python-version file is included.

Don't forget to install pip requirements: `pip install -r requirements.txt`

### Running

All projects are designed to be run as modules from the root directory, eg:

```bash
python -m theia.projects.palette_apply -h
```

### Continuous Integration

All PRs and commits are automatically checked using Github Actions.

Testing is done with the standard **unittest** library. To run tests from the root directory: `python -m unittest`

Formatting is done with [Black](https://github.com/psf/black). Style is checked as part of the CI process.

## Blender

Some of these scripts utilise Blender **2.91** to generate 3D models. In order for these scripts to function, you will need to have Blender installed and added to your PATH.

## Source Engine

Some of these scripts are designed to export content for use in the Source Engine - there's a bit more setup required for these.

### VTFCmd

To convert textures into the .vtf file format, VTFCmd.exe should be installed into the root directory.
You can grab this automatically by running `./scripts/install_vtfcmd.sh`

### Blender Plugins

Scripts that export models for Source Engine use the following plugins:

- [Blender Source Tools](https://github.com/Artfunkel/BlenderSourceTools)
- [VHAC-D](https://github.com/tpdickso/blender_vhacd)

if you're trying to get these working with 2.9 - good luck!
