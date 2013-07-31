import urllib2
import os
import time
import logging
import re

local_path = '/'.join(os.getcwd().split('/')[0 : -1])
parent_url = "http://dumps.wikimedia.org/other/pagecounts-raw/"
curr_file_name = None

def initLog
    log_file = '/'.join([path, 'log', 'wiki_log'])
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    
def downloadFile(url):
    file_name = '/'.join([file_path, 'data', url.split('/')[-1]])
    try:
        u = urllib2.urlopen(url)
    except:
        logging.debug(url, "cannot be opened.")
        return None
    start_time = time.time()
    with open(file_name, 'wb') as f:
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
    elapsed_time = time.time() - start_time
    logging.debug("Download time = ", elapsed_time)
    logging.debug("Download speed = ", file_size / elapsed_time)

def getStrFromURL(url, target):
    try:
        u = urllib2.urlopen(url)
    except:
        logging.debug(url, "cannot be opened.")
        return None
    html = u_parent.read()
    regex = re.compile('%s'%target)
    return [res.group(1) for res in re.finditer(regex, html)]


def generateURL():
    years = getStrFromURL(parent_url, '20\d{2}')
    if not years:
        return None
    year_url = '/'.join([parent_url, years[-1]])
    months = getStrFromURL(year_url, '20\d{2}-\d{2}')
    if not months:
        return None
    month_url = '/'.join([year_url, months[-1]])
    files = getStrFromURL(month_url, 'pagecounts-\d{8}-\d{6}.gz')
    if not files:
        return None
    if curr_file_name in files:
        start_idx = files.index(curr_file_name)
    else:
        start_idx = len(files) - 1
    file_url = []
    for file_name in files[start_idx:]:
        file_url.append('/'.join([month_url, file_name]))
    return file_url

