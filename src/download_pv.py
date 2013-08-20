import urllib2
import os
import time
import log
import re

local_path = '/'.join(os.getcwd().split('/')[0 : -1])
parent_url = "http://dumps.wikimedia.org/other/pagecounts-raw"
curr_file_name = None

def downloadFile(url):
    log.write("Download %s" %url)
    file_name = '/'.join([local_path, 'data', url.split('/')[-1]])
    try:
        u = urllib2.urlopen(url)
    except:
        log.write(i"%s cannot be opened." %url)
        return 
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
    log.write("Download time = %d sec" % elapsed_time)
    logg.write("Download speed = %f" % file_size / elapsed_time)

def getStrFromURL(url, target):
    try:
        u = urllib2.urlopen(url)
    except:
        log.write("%s cannot be opened." %url)
        return 
    html = u.read()
    regex = re.compile('%s'%target)
    return [res.group() for res in re.finditer(regex, html)]

def generateURL():
    years = getStrFromURL(parent_url, '20\d{2}')
    if not years:
        return 
    year_url = '/'.join([parent_url, max(years)])
    months = getStrFromURL(year_url, '20\d{2}-\d{2}')
    if not months:
        return 
    month_url = '/'.join([year_url, months[-1]])
    files = getStrFromURL(month_url, 'pagecounts-\d{8}-\d{6}.gz')
    if not files:
        return 
    if curr_file_name in files:
        start_idx = files.index(curr_file_name)
    else:
        start_idx = len(files) - 1
    file_url = []
    for file_name in files[start_idx:]:
        file_url.append('/'.join([month_url, file_name]))
    return file_url


def main():
    log.init()
    #l = generateURL()
    for url in generateURL():
        downloadFile(url)

if __name__ == "__main__":
    main()
