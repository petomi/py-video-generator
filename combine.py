# SETUP INSTRUCTIONS:
# Ensure Python 3.7+ is installed.
# Follow the steps here to install and activate the virtual env using venv:
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Then run `pip install -r requirements.txt`
# Uses either command line arguments or variables defined in config.yml file for configuration.

from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips
import argparse
import os, re
import yaml

# define optional command line arguments using argparse
parser = argparse.ArgumentParser(description='COMBINE.PY //// Combine some video clips via the command line.')
parser.add_argument('--root_directory_location', nargs='?', help='the root folder location of the video clips (non-relative).')
parser.add_argument('--output_file_location', nargs='?', help='the desired output file directory (relative).')
parser.add_argument('--unique_clip_id', nargs='?', help='the unique id to search for in each video clip name.')
parser.add_argument('--video_file_extension', nargs='?', help='the video file format (no period).')
parser.add_argument('--audio', nargs='?', help='full path to a background audio track that will overwrite the video clip audio.')

# assign params to namespace
args = parser.parse_args()

# get YAML config.yml file settings, accessed using cfg[key][subkey]
file = open('config.yml', 'r')
cfg = yaml.load(file, Loader= yaml.FullLoader)

# set up variables (command line overrides config.yml)
root_directory_location = args.root_directory_location or cfg['combine']['root_directory_location']
output_file_location = args.output_file_location or cfg['combine']['output_file_location']
unique_clip_id = args.unique_clip_id or cfg['combine']['unique_clip_id']
video_file_extension = args.video_file_extension or cfg['shared']['video_file_extension']
audio = args.audio or cfg['combine']['audio']

clips_to_join_list = []
output_file_name = 'render.mp4' # TODO
print("root directory selected: " + root_directory_location)

for root, subdirs, files in os.walk(root_directory_location):
    for filename in files:
        # check file for unique id and correct file type
        if re.match(rf"^.*{unique_clip_id}.*\.{video_file_extension}", filename, re.IGNORECASE):
            # get full file path
            file_path = os.path.join(root, filename)
            print("File added to concatenate: " + file_path)
            # load file as video clip into array
            clips_to_join_list.insert(len(clips_to_join_list), VideoFileClip(name_path))


# combine selected video clips in order they were discovered
final_render = concatenate_videoclips(clips_to_join_list)

# overwrite audio if selected
if audio != None and audio != '':
    print('Audio track selected: ' + audio)
    background_audio_clip = AudioFileClip(audio)
    final_render = final_render.set_audio(background_audio_clip)

# render to file
final_render.write_videofile(f'{output_file_location}/render.mp4', codec='libx264', fps=25)

# dump all clips from memory
for video_file in clips_to_join_list:
    video_file.close()

# print success message
print(f"All done! File exported to {output_file_location}.")
