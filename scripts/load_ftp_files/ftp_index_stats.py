#!/usr/binenv python3
'''
A script for reading index file from Blueprint's FTP site.
It populates a local MySQl database with metadata and file information.
Also this script checks if FTP files are accessible.
'''

import argparse,os
from ftplib import FTP
from tempfile import mkdtemp
from shutil import rmtree
from ftp_index_method import get_temp_dir,clean_temp_dir,get_ftp_index,read_index_file
from db_index import connect_db,update_index_db

parser=argparse.ArgumentParser()
parser.add_argument('-f','--ftp_url',    default='ftp.ebi.ac.uk',help='FTP url')
parser.add_argument('-l','--url_prefix', default='http://ftp.ebi.ac.uk/pub/databases/',help='URL prefix for files')
parser.add_argument('-d','--dir_path',   default='/pub/databases/blueprint/releases/current_release/homo_sapiens/',help='FTP path')
parser.add_argument('-i','--index_file', required=True,help='Name of index file from FTP')
parser.add_argument('-w','--work_dir',   required=True, help='Path to temp directory')
parser.add_argument('-o','--dbhost',     default='localhost', help='MySQL db hostname, default: localhost')
parser.add_argument('-P','--dbport',     default='3306', help='MySQL db port, default; 3306')
parser.add_argument('-u','--dbuser',     required=True,  help='MySQL db user name')
parser.add_argument('-p','--dbpass',     required=True,  help='MySQL db password')
parser.add_argument('-b','--dbname',     required=True,  help='MySQL db name')
args=parser.parse_args()

ftp_url=args.ftp_url
dir_path=args.dir_path
index_file=args.index_file
work_dir=args.work_dir
url_prefix=args.url_prefix

dbparams={'host':args.dbhost, 'user': args.dbuser,'password':args.dbpass,'db':args.dbname}
db_cursor=connect_db(dbparams)

try:
  temp_dir=get_temp_dir(work_dir=work_dir)
  os.chdir(temp_dir)
  get_ftp_index(ftp_url=ftp_url,dir=dir_path,index=index_file)
  index=read_index_file(index_file)
  update_index_db(db_cursor,index, url_prefix)  
      
except Exception as e:
  print('got error: %s' % e)
finally:
  clean_temp_dir(temp_dir)


