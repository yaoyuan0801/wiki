from sys import *
import glob
import redis
import gzip
import time
import heapq
from sets import Set
import urllib2
import log

special_page = Set(['Wikipedia','index.html', '_', 'undefined', \
'Undefined', 'Main_Page', 'edit', 'main_page', 'Portal:', \
'File:', 'Special:', '404_error','index.php', 'null'])
num_top = 100

def getFileList():
    return glob.glob("../data/*.gz")

def testPage(tmp):
    if tmp[0] != 'en':
        return False
    for str in special_page:
        if tmp[1].startswith(str):
            return False
    return True

def pageViewCount(files, r):
    page_count = {}
    heap = []
    for f_name in files:
        log.write("Start to Process %s" % f_name)
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
                #if not (i % 100000):
                #    print i / 100000,
                #    stdout.flush()
    #print
    log.write("Time to go through the file = %d sec"\
     %(time.time() - start_time))
    log.write("%d valid wiki pages processed" %i)
    start_time = time.time()
    for (k, v) in heap:
        r.zadd("wiki:last_hour", k, v)
    log.write("Time to write into redis = %d sec"\
     %(time.time() - start_time))

def pageViewToRedis(files):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    file_cnt = r.incr("wiki:file_count")
    start_time = time.time()
    page_view = {}
    i = 1
    for f_name in files:
        log.write("Start to Process %s" % f_name)
        with gzip.open(f_name) as f:
            for line in f:
                tmp = line.strip().split()
                cnt = int(tmp[2])
                if testPage(tmp):
                    i += 1
                    key = "wiki:page:" + tmp[1]
                    total_cnt = r.incrby(key, cnt)
                    #need to figure out the right data structure here
                    if total_cnt >= 500 * file_cnt:
                        page_view[tmp[1]] = cnt
                if i % 100000 == 0:
                    print i / 100000,
                    stdout.flush()
    print
    log.write("Time to go through the file = %d sec"\
     %(time.time() - start_time))
    log.write("Total number of pages that has %d visits or more = %d"\
     %(500 * file_cnt, len(page_view)))
    for cnt, page in sorted([(v,k) for k,v in page_view.items()], reverse = True):
        print urllib2.unquote(page), '--',cnt
    log.write("Time to go through the file = %d sec" %(time.time() - start_time))
     

def processPageView():
    log.write("\n")
    local_time = time.asctime(time.localtime(time.time()))
    log.write(local_time)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    files = getFileList()
    pageViewCount(files, r)

def main():
    log.init()
    processPageView()

if __name__ == "__main__":
    main()
