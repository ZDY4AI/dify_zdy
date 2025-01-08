### 要求
确保环境中存在：
- ffmpeg    下载地址：https://ffmpeg.org/download.html#build-linux

### 运行
终端运行
ffmpeg -i <源文件地址> -filter_complex "[0:v]colorkey=<背景RGB值>:0.1:0.1[ckout]" -map "[ckout]" -map 0:a -c:v libvpx-vp9 -b:v 2M -c:a libvorbis <目标文件地址（本项目在当前文件）> \Avatars.webm
