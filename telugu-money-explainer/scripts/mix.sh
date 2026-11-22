set -e
cd /home/user/workspace/episodes/ep02-wine-shop/audio
for f in bedA bedB bedC; do ffmpeg -nostdin -loglevel error -y -i music/$f.mp3 -af loudnorm=I=-20:TP=-3:LRA=11 -ar 48000 -ac 2 music/${f}_n.wav; done
ffmpeg -nostdin -loglevel error -y -i music/bedB_n.wav -i music/bedB_n.wav -filter_complex "[0][1]acrossfade=d=4:c1=tri:c2=tri" music/bedB_loop.wav
ffmpeg -nostdin -loglevel error -y -i voice.wav -af "loudnorm=I=-16:TP=-2:LRA=9,aresample=48000" -ac 1 voice_n.wav
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 voice_n.wav)
ffmpeg -nostdin -loglevel error -y -i voice_n.wav -i music/bedA_n.wav -i music/bedB_loop.wav -i music/bedC_n.wav -filter_complex "
[1]atrim=0:272.6,afade=t=out:st=270.0:d=2.6[a];
[2]atrim=0:179.6,afade=t=in:d=2.0,afade=t=out:st=177.0:d=2.6,adelay=270000|270000[b];
[3]atrim=0:97,afade=t=in:d=2.0,afade=t=out:st=91.0:d=5.5,adelay=446500|446500[c];
[a][b][c]amix=inputs=3:normalize=0:duration=longest,volume=-12dB,atrim=0:$DUR[m];
[0]asplit=2[v][sc];[sc]aformat=channel_layouts=stereo[scs];
[m][scs]sidechaincompress=threshold=0.02:ratio=5:attack=40:release=500:makeup=1[md];
[v]aformat=channel_layouts=stereo[vs];
[vs][md]amix=inputs=2:normalize=0:duration=first[mix]" -map "[mix]" -ar 48000 mix_raw.wav
J=$(ffmpeg -nostdin -i mix_raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
MI=$(echo "$J" | python3 -c "import sys,json;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -nostdin -loglevel error -y -i mix_raw.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:$MI:linear=true,alimiter=limit=0.79:attack=3:release=60:level=false" -ar 48000 -c:a aac -b:a 192k mix.m4a
ffmpeg -nostdin -i mix.m4a -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
