#!/usr/bin/env bash
# Concat rendered parts + mux with mix -> out/v2/final.mp4.  Usage: bash finish.sh <episodeDir>
set -e; EP=$1; cd "$EP/out/v2"
ls full.part*.mp4 | sort -V | sed 's/^/file /' > parts.txt
ffmpeg -nostdin -loglevel error -y -f concat -i parts.txt -c copy video_only.mp4
ffmpeg -nostdin -loglevel error -y -i video_only.mp4 -i ../../audio/mix.m4a -map 0:v -map 1:a -c copy -shortest -movflags +faststart final.mp4
ffprobe -v error -show_entries format=duration,size -of csv=p=0 final.mp4
