# py-video-generator

This is a collection of Python scripts designed to automate the process of collecting video files from a media API, stitching them together, and uploading the result to an Azure blob storage account.
While each script can be run separately as a command-line utility, the `generate.py` file is intended to be the entry point for the program.

## Installation
* Ensure that Python 3.7+ is installed on your machine.
* Follow the steps [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to install and activate the virtual env using venv.
* Run `pip install -r requirements.txt`

## Configuration and Running the utility
* Run the script using `py generate.py`.
* You may either add required arguments via the command line (see available args using the `-h` parameter) or via a YML config file with the name `config.yml`.

An example YML config file is provided below.
```
generate:
  api_url_pattern: '' # the media API from which you are pulling the videos you want to stitch, with `{UNIQUE_ID}` as a placeholder for unique ids.
  error_log_file: './errors.txt' # the text file which will be used to log errors.
  unique_ids_file: './ids.txt' # the file from which unique ids will be read and inserted into the media API. Finished videos will use this ID as the file name.
collect:
  api_url: '' # the media API from which you are pulling the videos you want to stitch, with `{UNIQUE_ID}` as a placeholder for unique ids.
  save_location: './downloaded' # the location within which to save 
  unique_clip_id: '' # the unique id used to collect specific video content (will be appended to the downloaded videos' filenames) (overwritten by unique ids from file in generate.py if present).
combine:
  root_directory_location: '' # the location where the downloaded video content to stitch together is saved
  output_file_location: './rendered'
  unique_clip_id: '' # the unique id used to collect specific video content (will be the filename of the completed file)
  audio: '' # optional - when specified, overwrites existing video clips' audio with the specified file in the finished render.
shared:
  video_file_extension: 'mp4' # the video file format for all video clips.
upload:
  azure:
    connection_string: '' # your Azure storage account's connection string
    container_name: '' # your Azure storage account's container name
  source_directory: './rendered' # the directory from which to upload video files
  unique_clip_id: '' #the unique id used to collect specific video content 

```
Note that each script has its own configuration section, but that `api_url_pattern` and `unique_ids_file` will overwrite any script-specific configuration variables when `generate.py` is run.
