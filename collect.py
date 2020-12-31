# SETUP INSTRUCTIONS:
# Ensure Python 3.7+ is installed.
# Follow the steps here to install and activate the virtual env using venv:
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Then run `pip install -r requirements.txt`
# Uses either command line arguments or variables defined in config.yml file for configuration.

import os, re
import yaml
import argparse
import requests

# define optional command line arguments using argparse
parser = argparse.ArgumentParser(description='COLLECT.PY //// Get media file URLs from an API endpoint and download them to disk.')
parser.add_argument('--save_location', nargs='?', help='the full path to the directory where media should be saved.')
parser.add_argument('--api_url', nargs='?', help='the API endpoint used to get the media URLS.')
parser.add_argument('--video_file_extension', nargs='?', help='the type of files we want to get from the API results.')
args = parser.parse_args()

# get YAML config.yml file settings, accessed using cfg[key][subkey]
file = open('config.yml', 'r')
cfg = yaml.load(file, Loader= yaml.FullLoader)

# set up variables (command line overrides config.yml)
save_location = args.save_location or cfg['collect']['save_location']
api_url = args.api_url or cfg['collect']['api_url']
video_file_extension = args.video_file_extension or cfg['shared']['video_file_extension']

try:
    # call API URL
    print(f'Calling media API: {api_url}')
    response = requests.get(api_url)

    # if API call failed, raise exception
    if (response.status_code != 200):
        raise Exception("API call failed: " + response.text)

    # parse API results to pull out a list of media urls ending with the correct file extension
    media_urls = re.findall(rf"https\:\/\/[A-Za-z0-9\/\.\-\_]*\.{video_file_extension}", response.text, re.IGNORECASE)

    if len(media_urls) > 0:
        print(f'Attempting to download media from API results to {save_location}.')
        # for each media in list, download to save directory (and flush from memory??)
        for url in media_urls:
            # get filename from url
            filename = re.search(rf"[A-Za-z0-9\.\-\_]*\.{video_file_extension}", url).group(0)
            # download to save directory
            # use streaming method, more optimized for threading than one at a time
            # see https://stackoverflow.com/questions/14270053/python-requests-not-clearing-memory-when-downloading-with-sessions
            request = requests.get(url, stream=True)
            with open(save_location + filename, 'wb') as code:
                for chunk in request.iter_content(1024):
                    if not chunk:
                        break
                    code.write(chunk)

            # # old method of downloading (not chunked)
            # r = requests.get(url, allow_redirects=True)
            # f = open(save_location + filename, 'wb').write(r.content)
            # f.close()
            print(f'Media file {filename} downloaded successfully.')
    else:
        print(f'No matching media URLs found in API results.')

except Exception as ex:
    print('Error downloading media:')
    print(ex)


