#!/bin/sh
# mix.sh <vo.mp3> <music.wav> <offset-ms> <seconds> <out.wav> — voice at -16 LUFS, the bed ducked under it
ffmpeg -loglevel error -y -i "$1" -i "$2" -filter_complex "[0:a]adelay=$3:all=1,loudnorm=I=-16:TP=-1.5:LRA=7,aresample=44100,apad,asplit=2[v1][v2];[1:a]volume=0.22[m];[m][v1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[md][v2]amix=inputs=2:normalize=0,atrim=0:$4,alimiter=limit=0.95[o]" -map "[o]" -ar 44100 -ac 2 "$5"
