#!/usr/bin/env python3

import os,sys
from ftplib import FTP
from tempfile import mkdtemp
from shutil import rmtree
from http.client import HTTPConnection
from urllib.parse import urlsplit


def get_temp_dir(work_dir,prefix='temp'):
  '''
  This function returns a temporary directory
  '''
  try:
    temp_dir=mkdtemp(prefix=prefix,dir=work_dir)
    return temp_dir
  except Exception as e:
    print('Error: %s' % e)
 
def clean_temp_dir(temp_dir): 
  '''
   This function delete a directory and all its contents
  '''
  if os.path.isdir(temp_dir):
    try :
      rmtree(temp_dir)
    except Exception as e:
       print('couldn\'t remove %s' % temp_dir)
    else:
      print('removed %s' % temp_dir)

def get_ftp_index(ftp_url='ftp.debian.org', dir='debian',index='README'):
  '''
  This function connect to a FTP server and retrieve a file
  '''
  with FTP(ftp_url) as ftp:
    ftp.login()
    ftp.cwd(dir)
    ftp.retrbinary('RETR '+index, open(index,'wb').write)
    ftp.quit()

def read_index_file(infile, f_header=[]):
  '''
     Read an index file and a list of fields (optional)
     Returns a list of dictionary 
  '''

  if len(f_header) == 0:
    f_header=['EXPERIMENT_ID','FILE_TYPE','SAMPLE_NAME','EXPERIMENT_TYPE','FILE','LIBRARY_STRATEGY']

  infile=os.path.abspath(infile)

  if os.path.exists(infile) == False:
    print('%s not found' % infile)
    sys.exit(2)

  with open(infile, 'r') as f:
    header=[]
    file_list=[]

    for i in f:
      row=i.split("\t")
      if(header):
        filtered_dict=dict((k,v) for k,v in dict(zip(header,row)).items() if k in header)
        file_list.append(filtered_dict)
      else:
        header=row
  return file_list

def check_ftp_url(full_url):
  '''
  This function checks if an url is accessible and returns its http response code
  '''
  url=urlsplit(full_url) 
  conn = HTTPConnection(url.netloc)
  conn.request("HEAD",url.path)
  res = conn.getresponse()
  return res.status
  
if __name__=='__main__':
  url='http://ftp.ebi.ac.uk/pub/databases/blueprint/data/homo_sapiens/GRCh38/Cell_Line/BL-2/Sporadic_Burkitt_lymphoma/ChIP-Seq/NCMLS/BL-2_c01.ERX297411.H3K4me1.bwa.GRCh38.20150528.bw'
  code=check_ftp_url(url)
  print(code)

