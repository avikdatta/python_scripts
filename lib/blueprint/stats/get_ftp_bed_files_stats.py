#!/usr/bin/env python3

import os, argparse, warnings
from shutil import rmtree
from ftplib import FTP
from tempfile import mkdtemp
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlsplit, urlunparse

def generate_bed_stats_from_index(index, exp_id, ftp_url, dir_prefix, work_dir):
  #Get file uri from index
  file_uri=get_bed_file(index=index,exp_id=exp_id)

  #Construct complete file uri
  file_uri=urlunparse(('http',ftp_url, dir_prefix + file_uri,'','',''))

  #Split dir and file path
  url=urlsplit(file_uri)
  (dir_path, file_path)=os.path.split(url.path)

  #Download bed file and generate stats and plots
  (data_list, output_file)=get_bed_stats(work_dir=work_dir,ftp_url=url.netloc, dir=dir_path, file=file_path, prefix=exp_id)
  return data_list, output_file

def get_bed_file(index,exp_id):
  all_data=pd.read_table(index)
  all_data=all_data.set_index('EXPERIMENT_ID')
  file_uri=all_data.loc[exp_id]['FILE'][all_data.loc[exp_id]['FILE'].str.contains('bed.gz')][exp_id]
  return file_uri

def plot_from_bed_count(data_list, output_file):
  df=pd.DataFrame(data_list,columns=['chr','count'])
  order_list=['chr1', 'chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10', 'chr11','chr12','chr13','chr14','chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22']
  df=df.set_index('chr')
  df=df.reindex(order_list)
  fig=plt.figure()
  df.plot(kind='bar',fontsize=8)
  fig.savefig(output_file)
  plt.close("all")
  
def read_bed_file(file):
  columns=['chr','start','end','name','score,', 'dot','fold_change','log10p','log10q','summit']
  data=pd.read_table(file, compression='gzip', header=None, names=columns, index_col='chr')
  chr_group=data.groupby(level=0)
  lists=[{'chr':chr,'count':len(chr_group.get_group(chr))} 
         for chr in chr_group.groups.keys()]
  return lists

def clean_temp_dir(temp_dir): 
  '''
   This function delete a directory and all its contents
  '''
  if os.path.isdir(temp_dir):
    try :
      rmtree(temp_dir)
    except Exception as e:
       warnings.warn('couldn\'t remove %s' % temp_dir)

def get_temp_dir(work_dir,prefix='temp'):
  '''
  This function returns a temporary directory
  '''
  try:
    temp_dir=mkdtemp(prefix=prefix,dir=work_dir)
    return temp_dir
  except Exception as e:
    print('Error: %s' % e)

def get_ftp_file(ftp_url, dir, file):
  '''
  This function connect to a FTP server and retrieve a file
  '''
  with FTP(ftp_url) as ftp:
    ftp.login()
    ftp.cwd(dir)
    ftp.retrbinary('RETR '+file, open(file,'wb').write)
    ftp.quit()

def read_ftp_file(work_dir, ftp_url, dir, file, use_temp_dir=True):
  json_list=[]
  try:
    if use_temp_dir:
      temp_dir=get_temp_dir(work_dir=work_dir)
      os.chdir(temp_dir)
    get_ftp_file(ftp_url=ftp_url, dir=dir, file=file)
    json_list=read_bed_file(file)
  except Exception as e:
    print('got error: %s' % e)
  finally:
    if use_temp_dir:
      os.chdir(work_dir)
      clean_temp_dir(temp_dir)
  return json_list
 
def get_bed_stats(work_dir, ftp_url, dir, file, prefix):
  '''
  Generate the lists of peak counts for ech chromosomes and a png cart file
  '''

  data_list=read_ftp_file(work_dir=work_dir,ftp_url=ftp_url, dir=dir, file=file)  
  output_file=os.path.join(work_dir, prefix+'.png')

  '''
  Do not generate plot for existing data, a speedup measure
  '''
  plot_from_bed_count(data_list=data_list, output_file=output_file)

  return data_list, output_file


