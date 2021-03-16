
import zipfile
import glob
import os
from urllib.parse import urljoin
import logging

zipfiles = glob.glob("*.zip")

if os.path.isdir('unzip') == False :
    os.mkdir('unzip')

logging.basicConfig(filename ='unzip.log',format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

errorzip = []
for zfile in zipfiles:
    print(zfile)
    print('unzipping' + zfile)
    try:
        with zipfile.ZipFile(zfile, 'r') as zip_ref:
            zip_ref.extractall('unzip')
        logging.info('unzip success' + zfile)
    except:
        errorzip.append(zfile)
        logging.info('unzip error ' + zfile)
logging.info('error zips' + str(errorzip))
