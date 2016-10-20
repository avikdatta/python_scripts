#!/usr/bin/env python3

import argparse
from db_index import connect_db
from ftp_index_method import get_temp_dir, clean_temp_dir
from blueprint.peak_correlation.peak_correlation import calculate_bedtool_jaccard, fetch_path_for_exp, fetch_file_by_rsync, generate_exp_pair, check_peak_interaction_db, store_peak_interaction_stat 

parser=argparse.ArgumentParser()
parser.add_argument('-i','--index_file', required=True, help='Index file containing the experiment and files information')
parser.add_argument('-w','--work_dir', required=True, help='Work directory')
parser.add_argument('-H','--mysql_host', default='localhost', help='MySQL server host name, default: localhost')
parser.add_argument('-P','--mysql_port', default='3306', help='MySQL server port id, default: 3306')
parser.add_argument('-n','--mysql_dbname', required=True, help='MySQL server database name')
parser.add_argument('-u','--mysql_user', required=True, help='MySQL server user name')
parser.add_argument('-p','--mysql_pass', required=True, help='MySQL server password name')
parser.add_argument('-U','--store_user', required=True, help='User name of storage server')
parser.add_argument('-I','--store_ip', required=True, help='Host IP address of storage server')

args=parser.parse_args()

work_dir     = args.work_dir
index_file   = args.index_file
store_user   = args.store_user
store_host   = args.store_ip
mysql_host   = args.mysql_host
mysql_user   = args.mysql_user
mysql_port   = args.mysql_port
mysql_pass   = args.mysql_pass
mysql_dbname = args.mysql_dbname

dbparams={'port': mysql_port, 'host': mysql_host, 'password': mysql_pass, 'user': mysql_user, 'db': mysql_dbname}

db_conn=connect_db(dbparams)

for exp_idA, exp_idB in generate_exp_pair(index_file=index_file):
  print('{0} : {1}'.format(exp_idA, exp_idB))
  val_exist=check_peak_interaction_db(db_conn=db_conn, exp_idA=exp_idA, exp_idB=exp_idB)

  # calculate value only its not present in db
  if not val_exist:
    try:
      # fetch file path info from db
      fileA=fetch_path_for_exp(db_conn=db_conn, exp_id=exp_idA)
      fileB=fetch_path_for_exp(db_conn=db_conn, exp_id=exp_idB)
     
      # get temp dir
      temp_dir=get_temp_dir(work_dir=work_dir)

      # fetch files by rsync
      local_fileA=fetch_file_by_rsync(user=store_user, host=store_host, source=fileA, dest_dir=temp_dir)
      local_fileB=fetch_file_by_rsync(user=store_user, host=store_host, source=fileB, dest_dir=temp_dir)

      # calculate Jaccard stats for pair of bed files
      data=calculate_bedtool_jaccard(bedA=local_fileA, bedB=local_fileB, f=0.95, r=True)
      # store intersection value in db
      store_peak_interaction_stat(db_conn=db_conn, exp_idA=exp_idA, exp_idB=exp_idB, data=data)
       
    except Exception as e:
      print('Got error {0}'.format(e))
    finally:
      clean_temp_dir(temp_dir)

db_conn.close()





