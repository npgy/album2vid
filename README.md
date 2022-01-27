# album2vid

If you run a YouTube channel for music like I do, you will find this useful.
It lets you generate an output video from audio files and their respective cover art reasonably fast.

## How to use
The simplest way to run this tool is to download the binary for your OS on the [releases](https://github.com/npgy/album2vid/releases) page. 
Unfortunately at the moment there is only a binary for Windows.  
You can also choose to just run the python script manually with your own binary of Ffmpeg.  

First make sure you have prepared your album's files correctly. They need to be ordered numerically and the cover art needs to have a particular name.
Here's an example of what that would look like:  

![Album file example](https://i.imgur.com/yqjylZX.png)

As you can see, the tracks have their numbers in front of them, and the cover art is named "cover.jpg".  
This program also accepts "cover.png".

Once you open the program, it will ask for the directory of your album's files. You can paste in the path url or just run the program inside that folder and hit enter.  
After it converts your audio files and cover art to a video, a file named "out.mp4" will appear. This is your final video, you are ready to upload!  
In addition, this program also generates a tracklist with timestamps for you! It will output to the file "tracklist.txt"

Some things to note are that this renders in x264 and 1080x1080. Your cover art must be 1:1 aspect ratio; most are.  

I hope anyone who comes across this finds it useful!

### Big thanks to:
Z from Nightride FM for help with FFMPEG  
HurleyBirdJr for creating the GUI (wip)
