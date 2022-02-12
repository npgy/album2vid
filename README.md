# album2vid

If you run a YouTube channel for music like I do, you will find this useful.
It lets you generate an output video from audio files and their respective cover art reasonably fast.

## Installation
The simplest way to install this tool is to download the binary for your OS on the [releases](https://github.com/npgy/album2vid/releases) page.  
You can also choose to just clone the python script and run it manually with your own binary of Ffmpeg. This should work on any OS.  

## Usage
`album2vid [-h] [-f] [path]`  

Flags:  
`-f` or `--fast`: Enables fast mode, may cause rendering errors.  
Essentially, without this flag, the program converts your input files to AAC first, and then stitches those into the output video.  

Args:  
`path`: The full path to the album's folder  
Make sure to enclose this in quotes

First make sure you have prepared your album's files correctly. They need to be ordered numerically and the cover art needs to have a particular name.

### Audio file compatability:
```.wav```
```.mp3```
```.m4a```
```.ogg```
```.flac```

#### Here's an example folder:  
![Album file example](https://i.imgur.com/yqjylZX.png)

As you can see, the tracks have their numbers in front of them, and the cover art is named "cover.jpg".  
This program also accepts "cover.png".

Once you open the program, it will ask for the directory of your album's files. You can paste in the path url or just run the program inside that folder and hit enter.  
After it converts your audio files and cover art to a video, a file named "out.mp4" will appear. This is your final video, you are ready to upload!  
In addition, this program also generates a tracklist with timestamps for you! It will output to the file "tracklist.txt"

## Compiling
To compile this python script I use PyInstaller, which can be installed via pip like so: `pip install pyinstaller`.  
Before you compile, make sure you grab the appropriate [ffmpeg binary](https://ffmpeg.org/download.html) for the system you are targeting.  
Once you have the ffmpeg binary and this script in the same folder, you can use the following PyInstaller command to compile it into one fat binary:  
- For x86 systems: `pyinstaller -F --add-binary="ffmpeg:." --target-arch=x86_64 album2vid.py`.  
- For arm64 systems: `pyinstaller -F --add-binary="ffmpeg:." --target-arch=arm64 album2vid.py`.  

The resulting executable should be found in the `dist/` directory.

## Notes
- Some things to note are that this renders in x264 and 1080x1080.  
- Your cover art must also be 1:1 aspect ratio; most are.  
- If a universal2 binary of ffmpeg exists for macOS, I would love to know as it would allow me to compile only one binary for macOS to support both architectures.

### Big thanks to:
Z from Nightride FM for help with FFMPEG  

### Projects that use this:
[album2vid-gui](https://github.com/HurleybirdJr/album2vid-gui) by HurleyBirdJr
