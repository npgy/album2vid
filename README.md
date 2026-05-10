# album2vid

If you run a YouTube channel for music like I do, you will find this useful.
It lets you generate an output video from audio files and their respective cover art reasonably fast.

ffmpeg binary sources:

- mac and linux from https://ffmpeg.martin-riedl.de/
- win amd64 from https://www.gyan.dev/ffmpeg/builds/#release-builds

## Installation

The simplest way to install this tool is to download the binary for your OS on the [releases](https://github.com/npgy/album2vid/releases) page.

## Usage

`album2vid [-h] [-f] [path]`

Flags:  
`-f` or `--fast`: Enables fast mode, may cause rendering errors.  
Essentially, without this flag, the program converts your input files to AAC first, and then stitches those into the output video.

Args:  
`path`: The full path to the album's folder  
Make sure to enclose this in quotes

First make sure you have prepared your album's files correctly. They need to be ordered numerically and the cover art needs to have a particular name.

### Audio file compatibility:

`.wav`
`.mp3`
`.m4a`
`.ogg`
`.flac`

#### Here's an example folder:

![Album file example](https://i.imgur.com/yqjylZX.png)

As you can see, the tracks have their numbers in front of them, and the cover art is named "cover.jpg".  
This program also accepts "cover.png".

After it converts your audio files and cover art to a video, a file named "out.mp4" will appear in the same directory you ran the command on. This is your final video, you are ready to upload!  
In addition, this program also generates a tracklist with timestamps for you! It will output to the file "tracklist.txt" in that same directory.

## Notes

- The output is rendered in x264 at 1080x1080.
- Your cover art must be 1:1 aspect ratio; most are.
- I'm not supporting macOS Intel anymore
- I am not supporting win arm64 yet

## Known Issues

- Certain image files cause the GPU acceleration to fail and thus the whole command, I haven't looked too far into this

### Big thanks to:

Z from Nightride FM for help with FFMPEG  
[Alexis Masson](https://github.com/Aveheuzed) for helping refactor, organize, and simplify the codebase

### Projects that use this:

[album2vid-gui](https://github.com/HurleybirdJr/album2vid-gui) by HurleyBirdJr
