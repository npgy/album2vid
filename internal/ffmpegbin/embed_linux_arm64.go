//go:build linux && arm64

package ffmpegbin

import _ "embed"

//go:embed ffmpeg-bin/ffmpeg-linux-arm64-8.1
var FFmpeg []byte

//go:embed ffmpeg-bin/ffprobe-linux-arm64-8.1
var FFprobe []byte
