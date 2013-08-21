#!/usr/bin/python

import MySQLdb
import os
import sys
import gzip

def initDB(db_name):
    try:
        con = MySQLdb.connect('localhost', 'testuser', 'testuser')
    except:
        print "Cannot connect to DB"
        sys.exit(1)
    cursor = con.cursor()
    sql = 'DROP DATABASE IF EXISTS %s' % db_name
    cursor.execute(sql)
    sql = 'CREATE DATABASE IF NOT EXISTS %s' % db_name
    cursor.execute(sql)
    sql = "USE %s" % db_name
    cursor.execute(sql)
    cursor.close()
    return con
    

def writeToNewTable(file_name, con, table_name):
    sql = '''CREATE TABLE ''' + table_name + ''' (
               id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
               page VARCHAR(100) NOT NULL,
               count INT UNSIGNED ZEROFILL
             )'''
    cursor = con.cursor()
    cursor.execute(sql)
    for line in file_name:
        tmp = line.split()
        sql = "INSERT INTO %s (page, count) VALUES (%%s, %%s)" %table_name
        cursor.execute(sql, (tmp[0], int(tmp[1])))
    cursor.close()

def dumpTable(con, table_name):
    cursor = con.cursor()
    sql = "SELECT * from %s" % table_name
    cursor.execute(sql)
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        print row[1], row[2]
    cursor.close()

def indexBy(con, table_name, index_name, col_name):
    cursor = con.cursor()
    sql = "CREATE INDEX %s ON %s (%s)" %(index_name, table_name, col_name)
    cursor.execute(sql)
    cursor.close()

def topCount(con, table_name, col_name):
    cursor = con.cursor()
    sql = "SELECT * from %s ORDER BY %s DESC LIMIT 100" % (table_name, col_name)
    cursor.execute(sql)
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        print row[1], row[2]
    cursor.close()
    

def main():
    table_name = 'test'
    test_file = '../data/test_data'
    con = initDB('testDB')
    with open(test_file, 'r') as file_name:
        writeToNewTable(file_name, con, table_name)
    #dumpTable(con, table_name)
    index_name = 'idx_count'
    col_name = 'count'
    indexBy(con, table_name, index_name, col_name)
    topCount(con, table_name, col_name)
    con.close()

if __name__ == "__main__":
    main()
