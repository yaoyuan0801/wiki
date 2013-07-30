from sys import *
import glob
import gzip
import heapq
from sets import Set
import urllib2
special_page = Set(['index.html', '_', 'undefined', 'Undefined', 'Main_Page', 'edit'])
num_top = 50

def getFileList():
    return glob.glob("/users/yaoyuan/Documents/wiki/data/*.gz")

def testPage(tmp):
    if tmp[0] != 'en':
        return False
    if tmp[1] in special_page:
        return False
    if tmp[1][0:8] == "Special:":
        return False
    if tmp[1][0:9] == "Wikipedia:":
        return False
    return True

def pageViewCount(files):
    page_count = {}
    heap = []
    for f_name in files:
        i = 0
        with gzip.open(f_name) as f: 
            for line in f:
                i += 1
                tmp = line.strip().split()
                cnt = int(tmp[2])
                if testPage(tmp) and (len(heap) < num_top or cnt > heap[0][0]):
                    #page_count[tmp[0]] = cnt
                    heapq.heappush(heap, (cnt, tmp[1]))
                if len(heap) > num_top:
                    heapq.heappop(heap)
                if not (i % 10000):
                    print i / 10000,
                    stdout.flush()
    print
    for cnt, page in sorted(heap):
        print urllib2.unquote(page), "--", cnt


def main():
    files = getFileList()
    pageViewCount(files)

if __name__ == "__main__":
    main()
