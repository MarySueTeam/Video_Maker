#!/bin/bash

rm -rf ./media/videos
rm -rf ./media/texts
rm -rf ./media/sounds/*.mp3
manim render main.py --custom_folders 