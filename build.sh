#!/bin/bash
pyinstaller --hiddenimport _cffi_backend run.py --name RogueThroughTheVeil --add-data src/gui/assets/*:src/gui/assets/
