#!/bin/bash
for i in {1..12};
do mkdir $i && ffmpeg -i $i.mp4 -r 1 -q:v 1 -vf scale=960:-1 -sws_flags lanczos $i/%04d.jpg;
done