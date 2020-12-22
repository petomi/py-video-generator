# SETUP INSTRUCTIONS:
# Ensure Python 3.7+ is installed.
# Follow the steps here to install and activate the virtual env using venv: 
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Then run `pip install -r requirements.txt`

# USAGE INSTRUCTIONS:
# run `py combine.py` + any of the following params, separated by spaces:
# params:
# 

from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips
import argparse
import os
import re

# define command line arguments using argparse
parser = argparse.ArgumentParser(description='COMBINE.PY //// Combine some video clips via the command line.')
parser.add_argument('root_directory_name', default='.', help='the root folder location of the video clips (non-relative).')
parser.add_argument('output_file_location', default='.', help='the desired output file location (relative).')
parser.add_argument('unique_clip_id', default='', help='the unique id to search for in each video clip name.')
parser.add_argument('video_file_extension', default='mp4', help='the video file format (no period).')
# optional arguments
parser.add_argument('--audio', nargs='?', help='full path to a background audio track that will overwrite the video clip audio.')

# assign params to namespace
args = parser.parse_args()
print(args)

clips_to_join_list = []
output_file_name = 'render.mp4' # TODO
print("root directory selected: " + args.root_directory_name)

for root, subdirs, files in os.walk(args.root_directory_name):
    for filename in files:
        # check file for unique id and correct file type
        if re.match(rf"^.*{args.unique_clip_id}.*\.{args.video_file_extension}", filename, re.IGNORECASE):
            # get full file path
            name_path = os.path.join(root, filename)
            print("File added to concatenate: " + name_path)
            # load file as video clip into array
            clips_to_join_list.insert(len(clips_to_join_list), VideoFileClip(name_path))


# combine selected video clips in order they were discovered
final_render = concatenate_videoclips(clips_to_join_list)

# TODO - not working yet
#overwrite audio if selected
if args.audio != None:
    print('Audio track selected: ' + args.audio)
    background_audio_clip = AudioFileClip(args.audio)
    final_render.set_audio(background_audio_clip)

# render to file
final_render.write_videofile('render.mp4', codec='libx264', fps=25)

# dump all clips from memory
for video_file in clips_to_join_list:
    video_file.close()

# print success message
print(f"All done! File exported to {args.output_file_location}.")
