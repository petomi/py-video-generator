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
import os
import re

# catch improper use of arguments and exit
if len(sys.argv) == 0 or len(sys.argv) > 3:
    print(
        '''
        combine.py USAGE:
        Please enter the command `py combine.py {root folder location of video clips},
        {output file location},
        {unique id inside video clip name},
        {video file format (no period)}`
        to generate your unique concatenated video clip. Only supports mp4s.
        '''
    )
    exit()

# assign params to variables
root_directory_name = sys.argv[0] or "."
output_file_location = sys.argv[1] or ""
unique_clip_id = sys.argv[2] or ""
video_file_extension = sys.argv[3] or "mp4"
clips_to_join_list = []

# walk through all subdirectories of root folder to find all files
for root, subdirs, files in os.walk(root_directory_name):
    for filename in files:
        # check file for unique id and correct file type
        if re.match(rf"^.*{unique_clip_id}.*\.{video_file_extension}", filename, re.IGNORECASE):
            # get full file path
            name_path = os.path.join(root, filename)
            # load file as video clip into array
            clips_to_join_list.insert(VideoFileClip(len(clips_to_join_list), name_path))

# render all clips in list together (in order they were discovered)
final_render = concatenate_videoclips(clips_to_join_list)
final_render.write_videofile('render.mp4', codec='libx264')

# dump all clips from memory
for video_file in clips_to_join_list:
    video_file.close()

# print success message
print(f"All done! File exported to {output_file_location}.")
