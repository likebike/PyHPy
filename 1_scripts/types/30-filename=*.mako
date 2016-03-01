#!/bin/bash -eu

# Example command-line args:  /home/user/mysite/3_build  /home/user/mysite/4_output/dev  blog/post1.html.mako
IN_DIR=$1
OUT_DIR=$2
REL_PATH=$3
TARGET="$OUT_DIR/${REL_PATH%.mako}"   # Chop off the .mako extension.
TARGET_DIR=$(dirname "$TARGET")

mkdir -p "$TARGET_DIR"
python -m pyhpy.cmd --template-dir="$IN_DIR" --module-dir="$IN_DIR" "$REL_PATH" >"$TARGET"

