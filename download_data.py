# Imports
import requests
import zipfile
import os

# Environment vars
URL = 'https://github.com/sstangl/openpowerlifting-static/raw/gh-pages/openpowerlifting-latest.zip'
PATH_ZIP = 'data/opl-data-main.zip'

# Functions
def download_url(url, path_output, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(path_output, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def unzip_file(path_input, path_output):
    with zipfile.ZipFile(path_input, "r") as zip_ref:
        zip_ref.extractall(path_output)

# Download data
download_url(URL, PATH_ZIP)

# Unzip data
unzip_file(PATH_ZIP, 'data')

# Delete zip
os.remove(PATH_ZIP)