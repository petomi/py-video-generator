# SETUP INSTRUCTIONS:
# Ensure Python 3.7+ is installed.
# Follow the steps here to install and activate the virtual env using venv:
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Then run `pip install -r requirements.txt`
# Uses either command line arguments or variables defined in config.yml file for configuration.

from multiprocessing import Process, ProcessError
from subprocess import run
import argparse
import yaml

# FUNCTION FOR CALLING COLLECT, COMBINE, AND UPLOAD AS SUBPROCESSES
def generate_video_using_id(id, api_url_pattern):
    print(f'Generating video for id: {id}')
    url = api_url_pattern.replace('{UNIQUE_ID}', id)
    # call collect.py to get video clips
    print(f'Collecting media for id: {id}')
    run(['py', 'collect.py', '--api_url', url, '--unique_clip_id', id])
    # call combine.py to combine and render the clips
    print(f'Rendering video for id: {id}')
    run(['py', 'combine.py', '--unique_clip_id', id])
    # call upload.py to upload the finished clips
    print(f'Uploading finished video for id: {id}')
    run(['py', 'upload.py', '--unique_clip_id', id])


# MAIN PROGRAM

# define optional command line arguments using argparse
parser = argparse.ArgumentParser(description='GENERATE.PY //// Generate videos based on cloud-hosted media accessible via API and upload the result to Azure.')
parser.add_argument('--unique_ids_file', nargs='?', help='the file containing a list of unique ids to generate videos for, each on a new line')
parser.add_argument('--api_url_pattern', nargs='?', help='the template for the media API we pull media from, which will have the unique ids interpolated into it. Use `{UNIQUE_ID}` as placeholder.')
args = parser.parse_args()

# get YAML config.yml file settings, accessed using cfg[key][subkey]
file = open('config.yml', 'r')
cfg = yaml.load(file, Loader= yaml.FullLoader)

# set up variables (command line overrides config.yml)
unique_ids_file = args.unique_ids_file or cfg['generate']['unique_ids_file']
api_url_pattern = args.api_url_pattern or cfg['generate']['api_url_pattern']

# read list of ids from file
print(f'Importing ids from: {unique_ids_file}')
with open(unique_ids_file, 'r') as f:
    id_list = f.read().splitlines() # used instead of readlines to remove \n characters

try:
    open_processes=[]
    # for each unique ID listed in the file specified in config, begin generating and uploading video as threaded process
    for id in id_list:
        p = Process(target=generate_video_using_id, args=(id, api_url_pattern)).start()
        open_processes.append(p)

    for process in open_processes:
        process.join()

        if process.exception:
            error, traceback = process.exception
            print(traceback)

    print('All video clips have been generated.')

except Exception as ex:
    print('Error generating videos:')
    print(ex)
