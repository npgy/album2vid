from glob import glob
import os
import subprocess

# FFMPEG binary location
ffmpeg = "ffmpeg"

# Ask user for album directory
dir = input("Enter the path to your album's audio and cover art (hit enter for current working directory): ")

# Verify directory is valid
if not (os.path.isdir(dir) or dir == ""):
    print("The directory could not be found")
    quit()

# Add trailing slash for expanding filenames
try:
    if dir[len(dir)-1] != "/":
        dir += "/"
except IndexError:
    pass

# Find all audio files in the directory
exts = ('wav', 'mp3', 'm4a', 'ogg', 'flac')
files = []
for ext in exts:
    files.extend(glob(dir+"*."+ext))

# Find cover art
cover = []
cover.extend(glob(dir+"cover.jpg"))
cover.extend(glob(dir+"cover.png"))
cover = cover[0]

# Sort the list of files
files.sort()

# Write all audio files to a temporary text document for ffmpeg
with open("files.txt", "w") as f:
    for file in files:
        f.write("file '"+file+"'\n")

# Generate FFMPEG command
cmd = [
    ffmpeg,
    "-y",
    "-loop",
    "1",
    "-framerate",
    "1",
    "-i",
    cover,
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    "files.txt",
    "-tune",
    "stillimage",
    "-shortest",
    "-fflags",
    "+shortest",
    "-max_interleave_delta",
    "100M",
    "-vf",
    "format=yuv420p",
    "-s",
    "1080x1080",
    "-b:a",
    "320k",
    dir+"out.mp4"
]

# Execute FFMPEG command and delete temporary file
subprocess.run(cmd)
os.remove("files.txt")
