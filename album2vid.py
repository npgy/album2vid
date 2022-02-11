# AUTHOR: Nicholas Preston (npgy)

from glob import glob
import os
import subprocess
import mutagen
import time
import argparse
from sys import exit, platform
import shutil

parser = argparse.ArgumentParser(description="A command line tool for generating videos from albums/tracks")
parser.add_argument('-f', '--fast', action='store_true', help="Enables fast mode, may cause rendering errors")
parser.add_argument("path", nargs="?", default="", help="The full path to the album's folder")
args = parser.parse_args()
args = parser.parse_args()

def get_runtime(filename):
    """Returns the runtime of a file

    ;param filename: the file's full path
    ;return: the file's runtime as a float
    """
    raw_info = mutagen.File(filename).info.pprint()
    runtime = float(raw_info.rsplit(', ', 1)[1].split(' ')[0])
    return runtime

def get_shortname(filename):
    """Returns just the file's name

    ;param filename: the file's full path
    ;return: the file's name
    """
    return filename.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]

def get_timestamp(seconds):
    """Returns the formatted timestamp

    ;param seconds: the length of time in seconds
    ;return: the formatted timestamp
    """
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def throw_error(text):
    print("ERROR: "+text)
    exit()

def cleanup():
    """
    Cleans up temporary files that may have been generated
    """

    # Try deleting temp directory
    try:
        shutil.rmtree(temp_dir, ignore_errors=True, onerror=None)
    except:
        throw_error("Error deleting the temp directory")

    try:
        # Remove unndeeded files list file
        os.remove(dir+"files.txt")
    except FileNotFoundError:
        pass

# FFMPEG binary location
ffmpeg = "ffmpeg"

# Fix command for linux systems
if platform == "linux":
    ffmpeg = "./"+ffmpeg

print("Welcome to album2vid!")

# Ask user for album directory
# dir = input("Enter the path to your album's audio and cover art (hit enter for current working directory): ")
dir = args.path

# Temp directory for first pass transcoding
temp_dir = dir+"/.temp"

# Verify directory is valid
if not (os.path.isdir(dir) or dir == ""):
    throw_error("The directory could not be found")

# print(f"Currently running in the directory: {os.getcwd()}")
print()

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
if len(files) == 0:
    throw_error("The audio files could not be found")

# Find cover art
cover = []
cover.extend(glob(dir+"cover.jpg"))
cover.extend(glob(dir+"cover.png"))
try:
    cover = cover[0]
except IndexError:
    throw_error("The cover photo could not be found")

# Sort the list of files
files.sort()

# Clean up temp files in case program was exited abruptly on last run
cleanup()

# Calculate tracklist with timestamps
with open(dir+"tracklist.txt", "w") as f:
    curr_time = 0.0
    for file in files:
        f.write(get_shortname(file)+" -- "+get_timestamp(curr_time)+"\n")
        curr_time += get_runtime(file)

# Write all audio files to a temporary text document for ffmpeg
with open(dir+"files.txt", "w") as f:
    for file in files:
        if not args.fast:
            file = f"{temp_dir}/{get_shortname(file)}.m4a"
        # This part ensures that any apostrophes are escaped
        file = file.split("'")
        if len(file) > 1:
            file = "'\\''".join(file)
        else:
            file = file[0]

        # Write the file line
        f.write("file '"+file+"'\n")

if not args.fast:
    # First pass to encode audio (this avoids errors in the final render)
    os.mkdir(temp_dir)
    for file in files:
        first_pass_cmd = f"""{ffmpeg} -i "{file}" -map 0 -map -v? -map V? -acodec aac -b:a 320k "{temp_dir}/{get_shortname(file)}.m4a" """
        subprocess.call(first_pass_cmd, shell=True)

# Construct FFMPEG command for final render
render_cmd = f'{ffmpeg} -hwaccel auto -y -loop 1 -framerate 1 -i "{cover}" -f concat -safe 0 -i "{dir}files.txt" -tune stillimage -shortest -fflags +shortest -max_interleave_delta 100M -vf format=yuv420p -s 1080x1080 -b:a 320k "{dir}out.mp4"'
subprocess.call(render_cmd, shell=True)

# Cleanup temporary files
cleanup()
