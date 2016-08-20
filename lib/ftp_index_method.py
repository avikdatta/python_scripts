import os,sys
from ftplib import FTP
from tempfile import mkdtemp
from shutil import rmtree

def get_temp_dir(work_dir,prefix='temp'):
  try:
    temp_dir=mkdtemp(prefix=prefix,dir=work_dir)
    return temp_dir
  except Exception as e:
    print('Error: %s' % e)
 
def clean_temp_dir(temp_dir): 
  if os.path.isdir(temp_dir):
    try :
      rmtree(temp_dir)
    except Exception as e:
       print('couldn\'t remove %s' % temp_dir)
    else:
      print('removed %s' % temp_dir)

def get_ftp_index(ftp_url='ftp.debian.org', dir='debian',index='README'):
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

