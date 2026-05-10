//go:build darwin && arm64

package ffmpegbin

import _ "embed"

//go:embed ffmpeg-bin/ffmpeg-darwin-arm64-8.1
var FFmpeg []byte

//go:embed ffmpeg-bin/ffprobe-darwin-arm64-8.1
var FFprobe []byte
