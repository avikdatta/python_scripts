#!/usr.bin/env python3

import os, argparse
import pymysql.cursors
import pandas as pd
from db_index import connect_db
from urllib.parse import urlsplit, urlunparse
from blueprint.stats.get_ftp_bed_files_stats import get_ftp_file, get_bed_file

parser=argparse.ArgumentParser()
parser.add_argument('-f','--ftp_url', default='ftp.ebi.ac.uk', help='FTP url, default=ftp.ebi.ac.uk')
parser.add_argument('-d','--dir_prefix', default='/pub/databases/', help='FTP directory, default=/pub/databases/')
parser.add_argument('-i','--index_file', required=True, help='Index file containing the experiment and files information')
parser.add_argument('-w','--download_dir', required=True, help='Bed file download directory')
parser.add_argument('-m','--mysql_host', default='localhost', help='MySQL server host name, default: localhost')
parser.add_argument('-P','--mysql_port', default='3306', help='MySQL server port id, default: 3306')
parser.add_argument('-n','--mysql_dbname', required=True, help='MySQL server database name')
parser.add_argument('-u','--mysql_user', required=True, help='MySQL server user name')
parser.add_argument('-p','--mysql_pass', required=True, help='MySQL server password name')
parser.add_argument('-t','--mysql_table', default='bed_files', help='MySQL table name name for loading bed file details')
args=parser.parse_args()

ftp_url    = args.ftp_url
dir_prefix = args.dir_prefix
index_file = args.index_file
work_dir   = args.download_dir
dbhost     = args.mysql_host
dbuser     = args.mysql_user
dbpass     = args.mysql_passmysql_pass
dbname     = args.mysql_dbname
dbport     = args.mysql_port
dbtable    = args.mysql_table

db_params={'host':dbhost, 'user':dbuser,'password':dbpass,'db':dbname, 'port':dbport}
db_cursor=connect_db(db_params)

def get_ftp_bed_files_from_index(index, ftp_url, dir_prefix, work_dir):
  '''
  This function reads the index file in chunk, 
  download bed files in the download directory  and 
  returns a generator for experiment and local file path information
  '''

  # Read data from index file in chunk of 4000 lines
  data=pd.read_table(index_file, chunksize=4000)
  
  # Get ChIP-Seq experiments for each chunk
  for data_chunk in data:
    chip_exps=data_chunk.groupby('LIBRARY_STRATEGY').get_group('ChIP-Seq').groupby('EXPERIMENT_ID').groups.keys()
  
    data_chunk=data_chunk.set_index('EXPERIMENT_ID')

    # Go to work dir
    os.chdir(work_dir)

  
    for exp_id in chip_exps:
      try:
        if type(data_chunk.loc[exp_id]['FILE']) is str:
          file_uri=data_chunk.loc[exp_id]['FILE']
        else:
          file_uri=data_chunk.loc[exp_id][data_chunk.loc[exp_id]['FILE'].str.contains('bed.gz')]['FILE'][exp_id]

        if file_uri.endswith('bed.gz'):
          # Process only bed files

          file_uri=urlunparse(('http',ftp_url, dir_prefix + file_uri,'','',''))
          url=urlsplit(file_uri)
          (dir_path, file_path)=os.path.split(url.path)

          # Download FTP file
          try:
            get_ftp_file(ftp_url=url.netloc, dir=dir_path, file=file_path)      
          except Exception as e:
            print('Download failed for exp: {0}, file:{1}'.format(exp_id, file_path))

          output_file=os.path.join(work_dir, file_path)

          # Check output file
          if not os.path.exists(output_file):
            raise Exception('file {0} not present'.format(output_file))

          yield exp_id, output_file
      except Exception as e:
        print('got error {0}'.format(e))
  

def db_store_bed_file(db_conn, exp_id, file, table_name='bed_files'):
  '''
  This function store the bed file information in a MySQL database table
  '''

  sql='''
      INSERT INTO `%s` ( `experiment_id`,  `filename`)
      VALUES (%s,%s)
      '''
  try:
    with db_conn.cursor() as cursor:
      cursor.execute(sql,(table_name, exp_id, file))
  except Exception as e:
    print('Error store file %s' % e)
  else:
    db_conn.commit()


output_bed_generator=get_ftp_bed_files_from_index(index=index_file, ftp_url=ftp_url, dir_prefix=dir_prefix, work_dir=work_dir)

for exp_id, file in output_bed_generator:
  db_store_bed_file(db_conn=db_cursor, exp_id=exp_id, file=file, table_name=dbtable) 

