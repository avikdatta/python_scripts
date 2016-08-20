#!/usr/bin/env python3
import pymysql.cursors

def connect_db(dbparams):
  '''
  Accept DB parameter hash
  Connect to DB using PyMySQL
  Returns cursor 
  '''
  try:
    print(dbparams)
    conn = pymysql.connect(**dbparams)
    return conn.cursor()
  except Exception as e:
    print('Error %s' % e) 

  
