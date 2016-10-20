#!/usr/bin/env python3

import os, sys
import pandas as pd
from pybedtools import BedTool

def calculate_bedtool_jaccard(bedA, bedB, **args):
  '''
  This function use pybedtools package for calculating jaccard stats
  between two bed files
  '''
  
  # check if files are present
  if not os.path.exists(bedA):
    sys.exit('bed file not found, {0}'.format(bedA))

  if not os.path.exists(bedB):
    sys.exit('bed file not found, {0}'.format(bedB))

  # load files
  bedA_obj=BedTool(bedA)
  bedB_obj=BedTool(bedB)
 
  
  # calculate jaccard stats
  
  jaccard_stats=bedA_obj.jaccard(bedB_obj, **args)
  
  return jaccard_stats

def fetch_path_for_exp(db_conn, exp_id):
  '''
  
  '''

  sql='''
      select filename from bed_files where experiment_id = %s
      '''
  try:
    with db_conn.cursor() as cursor:
      hit_count=cursor.execute(sql,(exp_id))
      
      if hit_count > 1:
        raise Exception('more than one file found for {0}'.format(exp_id))
      filepath=(cursor.fetchone())[0]
  except Exception as e:
    print('error is: {0}'.format(e))
 
  return filepath

def fetch_file_by_rsync(user, host, source, dest_dir, **args):
  '''

  '''

  source_path='{0}@{1}:{2}'.format(user, host, source)
 
  (dir_path,file_path)=os.path.split(source)
  dest_path=os.path.join(dest_dir, file_path)

  options_str=''
  for arg_key, arg_value in args.items():
    if type(arg_value)==bool:
      options_str +=' --{0} '.format(arg_key)
    else:
      options_str +=' --{0}={1} '.format(arg_key, arg_value)
 
  rsync_cmd='rsync {0} {1} {2}'.format( options_str, source_path, dest_path )
  try:
    os.system(rsync_cmd)
  except Exception as e:
    print('Got error: {0}'.format(e))
  else:
    return dest_path

def generate_exp_pair(index_file):
  '''

  '''
  index_data=pd.read_table(index_file, chunksize=4000)
  
  experiment_set = set()

  # read data in chunk of 4000 lines
  for data_chunk in index_data:

    # get groupby object
    chip_exps=data_chunk.groupby('LIBRARY_STRATEGY').get_group('ChIP-Seq').groupby('EXPERIMENT_ID').groups.keys()
   
    # re-index dataframe
    data_chunk=data_chunk.set_index('EXPERIMENT_ID')
    
    # get unique set of experiment ids with bed file, i.e excluding Input
    for exp_id in chip_exps:
      try:
        if type(data_chunk.loc[exp_id]['FILE']) is str:
          file_uri=data_chunk.loc[exp_id]['FILE']
        else:
          file_uri=data_chunk.loc[exp_id][data_chunk.loc[exp_id]['FILE'].str.contains('bed.gz')]['FILE'][exp_id]

        if file_uri.endswith('bed.gz'):
          experiment_set.add(exp_id)

      except Exception as e:
        print('Error in data block:{0}'.format(e))
 

  
  for exp_id1 in experiment_set:
    for exp_id2 in experiment_set:
      if exp_id1 != exp_id2:
        yield (exp_id1, exp_id2)


def check_both_peak_interaction_db(db_conn, exp_idA, exp_idB):
  '''
  
  '''
  val_exist=False
  val_exist=check_peak_interaction_db(db_conn, exp_idA, exp_idB)
   
  if not val_exist:
    val_exist=check_peak_interaction_db(db_conn, exp_idB, exp_idA) 
 
def check_peak_interaction_db(db_conn, exp_idA, exp_idB):
  '''

  '''
  sql='''
      SELECT * from `peak_intersection` 
      where 
      `experiment_idA` = %s AND 
      `experiment_idB` = %s
      '''
  
  val_exist=False

  with db_conn.cursor() as cursor:
    try:
      cursor.execute(sql,(exp_idA, exp_idB))
      hit_count=cursor.fetchall()
    except Exception as e:
      print('got errpt {0}'.format(e))

  if hit_count:
    val_exist=True

  return val_exist

def store_peak_interaction_stat(db_conn, exp_idA, exp_idB, data):
  '''

  '''
  sql='''
      INSERT INTO `peak_intersection` ( `experiment_idA`, `experiment_idB`, 
      `jaccard`, `n_intersections`) VALUES ( %s, %s, %s, %s)
      '''

  jaccard_val=data['jaccard']
  n_intersections=data['n_intersections']

  with db_conn.cursor() as cursor:
    try:
      # insert value of A, B
      cursor.execute(sql, (exp_idA, exp_idB, jaccard_val, n_intersections))

      # insert value of B, A
      cursor.execute(sql, (exp_idB, exp_idA, jaccard_val, n_intersections))
    except Exception as e:
      print('Got error: {0}'.format(e))
    else:
      db_conn.commit()
      
  
