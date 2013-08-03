from sys import *
import glob
import redis
import gzip
import time
import heapq
from sets import Set
import urllib2
special_page = Set(['Wikipedia','index.html', '_', 'undefined', \
'Undefined', 'Main_Page', 'edit', 'main_page'])
num_top = 50

def getFileList():
    return glob.glob("../data/*.gz")

def testPage(tmp):
    if tmp[0] != 'en':
        return False
    if tmp[1] in special_page:
        return False
    if tmp[1].startswith("Special:") or tmp[1].startswith("Wikipedia:"):
        return False
    return True

def pageViewCount(files):
    page_count = {}
    heap = []
    for f_name in files:
        i = 1
        with gzip.open(f_name) as f: 
            for line in f:
                tmp = line.strip().split()
                cnt = int(tmp[2])
                if testPage(tmp):
                    i += 1
                    if (len(heap) < num_top or cnt > heap[0][0]):
                        heapq.heappush(heap, (cnt, tmp[1]))
                if len(heap) > num_top:
                    heapq.heappop(heap)
                if not (i % 100000):
                    print i / 100000,
                    stdout.flush()
    print
    for cnt, page in sorted(heap):
        print page, urllib2.unquote(page), "--", cnt
    print i

def pageViewToRedis(files):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    file_cnt = r.incr("wiki:file_count")
    start_time = time.time()
    page_view = {}
    i = 1
    for f_name in files:
        with gzip.open(f_name) as f:
            for line in f:
                tmp = line.strip().split()
                cnt = int(tmp[2])
                if testPage(tmp):
                    i += 1
                    key = ':'.join(["wiki:page:", tmp[1]])
                    total_cnt = r.incrby(key, cnt)
                    # 500 per hour is not bad for a wiki page
                    if total_cnt >= 500 * file_cnt:
                        page_view[tmp[1]] = cnt
                if i % 10000 == 0:
                    print i / 10000,
    print
    print "Time to go through the file = %d sec" %(time.time() - start_time)
    print "Total number of pages that has %d visits or more = %d" %(500 * file_cnt, len(page_view))
    for page, cnt in sorted([(v,k) for k,v in page_view.items()], reverse=True):
        print urllib2.unquote(page), '--',cnt
    print "Time to go through the file = %d sec" %(time.time() - start_time)
     

def main():
    files = getFileList()
    pageViewToRedis(files)

if __name__ == "__main__":
    main()
