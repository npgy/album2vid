from glob import glob
import os
import subprocess
import mutagen
import time

def get_runtime(filename):
    """Returns the runtime of a file
    
    ;param filename: the file's full path
    ;return: the file's runtime as a float
    """
    raw_info = mutagen.File(filename).info.pprint()
    runtime = float(raw_info.split(', ')[1].split(' ')[0])
    return runtime

def get_shortname(filename):
    """Returns just the file's name
    
    ;param filename: the file's full path
    ;return: the file's name
    """
    return filename.split('/')[-1].split('\\')[-1].split('.')[0]

def get_timestamp(seconds):
    """Returns the formatted timestamp
    
    ;param seconds: the length of time in seconds
    ;return: the formatted timestamp
    """
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

# FFMPEG binary location
ffmpeg = "ffmpeg"

# Ask user for album directory
dir = input("Enter the path to your album's audio and cover art (hit enter for current working directory): ")

# Temp directory for first pass transcoding
temp_dir = dir+"/.temp"

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

# Calculate tracklist with timestamps
with open(dir+"tracklist.txt", "w") as f:
    curr_time = 0.0
    for file in files:
        f.write(get_shortname(file)+" -- "+get_timestamp(curr_time)+"\n")
        curr_time += get_runtime(file)

# Write all audio files to a temporary text document for ffmpeg
with open(dir+"files.txt", "w") as f:
    for file in files:
        file = f"{temp_dir}/{get_shortname(file)}.m4a"
        # This part ensures that any apostrophes are escaped
        file = file.split("'")
        if len(file) > 1:
            file = "'\\''".join(file)
        else:
            file = file[0]
        
        # Write the file line
        f.write("file '"+file+"'\n")

# First pass to encode audio (this avoids errors in the final render)
os.mkdir(temp_dir)
for file in files:
    first_pass_cmd = f"""{ffmpeg} -i "{file}" -map 0 -map -v? -map V? -acodec aac -b:a 320k "{temp_dir}/{get_shortname(file)}.m4a" """
    subprocess.run(first_pass_cmd)

# Construct FFMPEG command for final render
render_cmd = f"{ffmpeg} -y -loop 1 -framerate 1 -i {cover} -f concat -safe 0 -i {dir}files.txt -tune stillimage -shortest -fflags +shortest -max_interleave_delta 100M -vf format=yuv420p -s 1080x1080 -b:a 320k {dir}out.mp4"
subprocess.run(render_cmd)

# Remove unndeeded files list file
os.remove(dir+"files.txt")

# Remove temp dir
for file in files:
    try:
        os.remove(f"{temp_dir}/{get_shortname(file)}.m4a")
    except FileNotFoundError:
        pass
os.rmdir(temp_dir)