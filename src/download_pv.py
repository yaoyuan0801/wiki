import urllib2
import os
import time
import logging
import re

local_path = '/'.join(os.getcwd().split('/')[0 : -1])
parent_url = "http://dumps.wikimedia.org/other/pagecounts-raw/"

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

def generateURL():
    try:
        u_parent = urllib2.urlopen(parent_url)
    except:
        logging.debug(parent_url, "cannot be opened.")
        return None
    parent_html = u_parent.read()
    match_year = re.finditer(r'20\d{2}', parent_html)
    year = [match.group(1) for match in match_year][-1]
    year_url = '/'.join([parent_url, year])
    try:
        u_year = urllib2.urlopen(year_url)
    except:
        logging.debug(year_url, "cannot be opened.")
        return None
    year_html = u_year.read()
    match_month = re.finditer(r'20\d{2}-\d{2}', year_html)
    month = [match.group(1) for match in match_month][-1]
    month_url = '/'.join([year_url, month])
    try:
        u_month = urllib2.urlopen(month_url)
    except:
        logging.debug(month_url, "cannot be opened.")
        return None
    month_html = u_month.read()
    match_file = re.finditer(r'pagecounts-\d{8}-\d{6}.gz'}, month_html)
    file_name = [match.group(1) for match in match_month][-1]
    file_url = '/'.join([month_url, file_name])
    return file_url

