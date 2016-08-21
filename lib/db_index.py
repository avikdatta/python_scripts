#!/usr/bin/env python3
import pymysql.cursors
import os,sys
from ftp_index_method import check_ftp_url

def connect_db(dbparams):
  '''
  Accept DB parameter hash
  Connect to DB using PyMySQL
  Returns connection 
  '''
  try:
    conn = pymysql.connect(**dbparams)
    return conn
  except Exception as e:
    print('Error %s' % e) 

def update_index_db(db_conn,index, url_prefix):
  '''
  This function accept a db connection, aindex file and url_prefix
  It checks if the files are already stored in db and store the new files
  '''
  db_cursor=db_conn.cursor()
  for line in index:
    file=line['FILE']
    filename=os.path.basename(file)
    existing_flag=None
    existing_flag=check_existing_file_in_db(db_conn,filename)
    if not existing_flag:
      store_file(db_conn, filename, line, url_prefix)


def store_file(db_conn, filename, line, url_prefix):
  '''
  This method stores the file in MySQL db
  '''
  exp_id=line['EXPERIMENT_ID']
  file=line['FILE']
  file_type=line['FILE_TYPE']
  file_md5=line['FILE_MD5']
  file_url=url_prefix+file 
  exp_type=line['EXPERIMENT_TYPE']
  sample_name=line['SAMPLE_NAME']
  lib_strategy=line['LIBRARY_STRATEGY']
  sql='''
      INSERT INTO `ftp_index_file` (`filename`,        `experiment_id`,  `sampe_name`,
                                    `library_strategy`,`experiment_type`,`file_url`,
                                    `file_md5`,        `file_type`,      `is_active` ) 
                                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
      '''

  ftp_file_status=check_ftp_url(file_url)
  if ftp_file_status == 200:
    try:
      with db_conn.cursor() as cursor:
        cursor.execute(sql,(filename,exp_id,sample_name,lib_strategy,exp_type, file_url,file_md5,file_type,'1'))
    except Exception as e:
      print('Error store_file %s' % e)
    else:
      db_conn.commit() 
  else:
    print('Got HTTP code %s for file %s' % (ftp_file_status, file_url)) 


def check_existing_file_in_db(db_conn,filename):
  '''
  This method checks if the file is already present in database
  '''
  try:
    with db_conn.cursor() as cursor:
      sql = "select * from ftp_index_file where filename=%s"
      cursor.execute(sql,(filename,))
      result=cursor.fetchall()
      return result
  except Exception as e:
     print('Error check_existing_file_in_db %s' % e)

