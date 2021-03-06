# SETUP INSTRUCTIONS:
# Ensure Python 3.7+ is installed.
# Follow the steps here to install and activate the virtual env using venv:
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Then run `pip install -r requirements.txt`
# Uses either command line arguments or variables defined in config.yml file for configuration.

import multiprocessing as mp
from subprocess import run
import argparse
import yaml

# define optional command line arguments using argparse
parser = argparse.ArgumentParser(description='GENERATE.PY //// Generate videos based on cloud-hosted media accessible via API and upload the result to Azure.')
parser.add_argument('--unique_ids_file', nargs='?', help='the file containing a list of unique ids to generate videos for, each on a new line')
parser.add_argument('--api_url_pattern', nargs='?', help='the template for the media API we pull media from, which will have the unique ids interpolated into it. Use `{UNIQUE_ID}` as placeholder.')
parser.add_argument('--error_log_file', nargs='?', help='the location of the error log file.')
args = parser.parse_args()

# get YAML config.yml file settings, accessed using cfg[key][subkey]
file = open('config.yml', 'r')
cfg = yaml.load(file, Loader= yaml.FullLoader)

# set up variables (command line overrides config.yml)
unique_ids_file = args.unique_ids_file or cfg['generate']['unique_ids_file']
api_url_pattern = args.api_url_pattern or cfg['generate']['api_url_pattern']
error_log_file = args.error_log_file or cfg['generate']['error_log_file']

# FUNCTION FOR CALLING COLLECT, COMBINE, AND UPLOAD AS SUBPROCESSES
def generate_video_using_id(id, api_url_pattern):
    try:
        print(f'Generating video for id: {id}')
        url = api_url_pattern.replace('{UNIQUE_ID}', id)
        # call collect.py to get video clips
        collect = run(['py', 'collect.py', '--api_url', url, '--unique_clip_id', id], capture_output=True)
        if len(collect.stderr) > 0:
            print(f'Error collecting media video with id: {str(id)}. {collect.stderr}')
            raise Exception(f'Error collecting media video with id: {str(id)}')
        # call combine.py to combine and render the clips
        # no error checking here because the video rendering library apparently throws false positive errors on completion of successful render.
        # we will check whether the correct file exists as part of the upload step and thus catch a render error.
        combine = run(['py', 'combine.py', '--unique_clip_id', id], capture_output=True)
        # call upload.py to upload the finished clips
        upload = run(['py', 'upload.py', '--unique_clip_id', id], capture_output=True)
        if len(upload.stderr) > 0:
            print(f'Uploading failed for video with id: {str(id)}. {upload.stderr}')
            raise Exception(
                f'Uploading failed for video with id {str(id)}')
    except Exception as ex:
        print(ex)
        raise Exception(ex)

# LOG FAILED RESULTS
def log_failed_results(result):
    with open(error_log_file, 'a+') as l:
        l.write('\n' + str(result))

# MAIN PROGRAM

if __name__ == '__main__':
    # read list of ids from file
    print(f'Importing ids from: {unique_ids_file}')
    with open(unique_ids_file, 'r') as f:
        id_list = f.read().splitlines() # used instead of readlines to remove \n characters

    pool = mp.Pool()

    try:
        # for each unique ID listed in the file specified in config, begin generating and uploading video as threaded process
        for id in id_list:
            if len(id) > 0:
                pool.apply_async(generate_video_using_id, args=(id, api_url_pattern), error_callback=log_failed_results)

        pool.close()
        pool.join()

        print('Script finished.')

    except Exception as ex:
        print('Error generating videos:')
        print(ex)
