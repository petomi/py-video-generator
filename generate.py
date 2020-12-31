# SETUP INSTRUCTIONS:
# Ensure Python 3.7+ is installed.
# Follow the steps here to install and activate the virtual env using venv:
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Then run `pip install -r requirements.txt`
# Uses either command line arguments or variables defined in config.yml file for configuration.

# This script calls collect.py to collect videos, then combine.py to combine and render them, and finally upload.py to upload them to Azure.

### Using a common API URL template specified in config,
### For each unique ID listed in the file specified in config (or via command line)
### Call collect.py to get video clips
### Call combine.py to combine and render the clips
### Call upload.py to upload the finished clips.

