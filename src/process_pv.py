from sys import *
import glob
import redis
import gzip
import time
import heapq
from sets import Set
import urllib2
#import log

special_page = Set(['Wikipedia','index.html', '_', 'undefined', \
'Undefined', 'Main_Page', 'edit', 'main_page', 'Portal:', \
'File:', 'Special:', '404_error','index.php', 'null', 'Windex.php'])
num_top = 10000
redis_name_dest = "wiki:hourly_page_view"

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
    for f_name in files:
        redis_dest = 'wiki:' + f_name
        #need to pop out the old ones?
        r.lpush(redis_name_dest, redis_dest)
        heap = []
        with gzip.open(f_name) as f: 
            for line in f:
                tmp = line.strip().split()
                cnt = int(tmp[2])
                if testPage(tmp):
                    if (len(heap) < num_top or cnt > heap[0][0]):
                        heapq.heappush(heap, (cnt, tmp[1]))
                if len(heap) > num_top:
                    heapq.heappop(heap)
        for k, v in heap:
            r.zadd(redis_dest, v, k)
        #print urllib2.unquote(v), k

def pageViewStat(r):
    M = r.zrange(redis_dest, 0, -1, withscores = 1)
    print "min: %s : %d" % (urllib2.unquote(M[0][0]), int(M[0][1]))
    print "max: %s : %d" % (urllib2.unquote(M[-1][0]), int(M[-1][1]))
    cnt = [float(x[1]) for x in M]
    print "mean = %f" % (sum(cnt) / len(cnt))
    print "median = %f " % cnt[len(cnt) / 2]
    for i in xrange(0, len(M)):
        if i % 100 == 0:
            print "%d-th %s : %d"% (i, urllib2.unquote(M[i][0]), int(M[i][1]))
            
    

def processPageView():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool = pool)
    r.flushdb()
    start_time = time.time()
    files = getFileList()
    pageViewCount(files, r)
    #pageViewStat(r)
    print "total_time = %d s" % (time.time() - start_time)

def main():
    processPageView()

if __name__ == "__main__":
    main()
