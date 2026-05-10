//go:build windows && amd64

package ffmpegbin

import _ "embed"

//go:embed ffmpeg-bin/ffmpeg-win-amd64-8.1.1
var FFmpeg []byte

//go:embed ffmpeg-bin/ffprobe-win-amd64-8.1.1
var FFprobe []byte
