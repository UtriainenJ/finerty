#!/bin/bash
set -e # Exit immediately if a command fails

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
SOURCE_DIR="$SCRIPT_DIR"
TARGET_DIR="$XDG_CONFIG_HOME/xkb"

mkdir -p "$TARGET_DIR/symbols" "$TARGET_DIR/rules"

cp -rv "$SOURCE_DIR/symbols/." "$TARGET_DIR/symbols/"
cp -rv "$SOURCE_DIR/rules/." "$TARGET_DIR/rules/"

echo "install script done"
