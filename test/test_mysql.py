#!/usr/bin/python

import MySQLdb
import os
import sys

def writeToNewTable(file_name, con, table_name):
    cursor = con.cursor()
    cursor.execute('DROP DATABASE IF EXISTS test')
    sql = 'CREATE DATABASE test IF NOT EXISTS'
    cursor.execute(sql)
    cursor.execute('')
    sql = '''CREATE TABLE ''' + table_name + ''' (
               id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
               page VARCHAR(100) NOT NULL,
               count UNSIGNED ZEROFILL
             )'''
    cursor.execute(sql)
    for line in file_name:
        tmp = line.split()
        cursor.execute("INSERT INTO testdb (%s, %s)", tmp[0], tmp[1])
    cursor.close()

def dumpTable(con, table_name):
    cursor = con.cursor()
    cursor.execute("SELECT * from %s", table_name)
    for i in range(cursor.rowcount):
        row = cur.fetchone()
        print row
    cursor.close()

def main():
    file_name = '../data/test_data'
    table_name = 'test'
    try:
        con = MySQLdb.connect('localhost', 'testuser', 'testuser')
    except:
        print "Cannot connect to DB"
        sys.exit(1)
    writeToNewTable(file_name, con, table_name)
    dumpTable(con, table_name)
    con.close()

if __name__ == "__main__":
    main()
