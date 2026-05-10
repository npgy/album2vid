//go:build linux && amd64

package ffmpegbin

import _ "embed"

//go:embed ffmpeg-bin/ffmpeg-linux-amd64-8.1
var FFmpeg []byte

//go:embed ffmpeg-bin/ffprobe-linux-amd64-8.1
var FFprobe []byte
