#!/bin/bash

if [ "$2" = "background" ]; then
    blender --background --python $1
else
    blender --python $1
fi