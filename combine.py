# SETUP INSTRUCTIONS:
# Ensure Python 3.7+ is installed.
# Follow the steps here to install and activate the virtual env using venv: 
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Then run `pip install -r requirements.txt`

# USAGE INSTRUCTIONS:
# run `py combine.py` + any of the following params, separated by spaces:
# params:
# 

from moviepy.editor import VideoFileClip, concatenate_videoclips
import argparse
import sys
import os
import re

# define command line arguments using argparse
parser = argparse.ArgumentParser(description='Combine some video clips via the command line.')
parser.add_argument('root_directory_name', help='The root folder location of the video clips.')
parser.add_argument('output_file_location', help='The desired output file location.')
parser.add_argument('unique_clip_id', help='The unique id to search for in each video clip name.')
parser.add_argument('video_file_extension', help='The video file format (no period)')

# assign params to namespace
args = parser.parse_args()
clips_to_join_list = []

print("root directory selected: " + args.root_directory_name)
# for root, subdirs, files in os.walk(args.root_directory_name):
#     for filename in files:
#         print ("file added:" + filename)
# walk through all subdirectories of root folder to find all files
for root, subdirs, files in os.walk(args.root_directory_name):
    for filename in files:
        # check file for unique id and correct file type
        if re.match(rf"^.*{args.unique_clip_id}.*\.{args.video_file_extension}", filename, re.IGNORECASE):
            # get full file path
            name_path = os.path.join(root, filename)
            print("file added to concatenate: " + name_path)
            # load file as video clip into array
            clips_to_join_list.insert(len(clips_to_join_list), VideoFileClip(name_path))

# render all clips in list together (in order they were discovered)
final_render = concatenate_videoclips(clips_to_join_list)
final_render.write_videofile('render.mp4', codec='libx264')

# dump all clips from memory
for video_file in clips_to_join_list:
    video_file.close()

# print success message
print(f"All done! File exported to {args.output_file_location}.")
