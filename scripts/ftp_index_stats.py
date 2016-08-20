import argparse,os
from ftplib import FTP
from tempfile import mkdtemp
from shutil import rmtree
from ftp_index_method import get_temp_dir,clean_temp_dir,get_ftp_index,read_index_file

parser=argparse.ArgumentParser()
parser.add_argument('-f','--ftp_url',  default='ftp.ebi.ac.uk')
parser.add_argument('-d','--dir_path', default='/pub/databases/blueprint/releases/current_release/homo_sapiens/')
parser.add_argument('-i','--index_file', required=True)
parser.add_argument('-w','--work_dir',   required=True)
args=parser.parse_args()

ftp_url=args.ftp_url
dir_path=args.dir_path
index_file=args.index_file
work_dir=args.work_dir

try:
  temp_dir=get_temp_dir(work_dir=work_dir)
  os.chdir(temp_dir)
  print('Now in %s' % temp_dir)
  get_ftp_index(ftp_url=ftp_url,dir=dir_path,index=index_file)
  print('downloaded ftp file %s' % index_file)
  index=read_index_file(index_file,['EXPERIMENT_ID','FILE'])
  exp_id=index[0]['EXPERIMENT_ID']
  file=index[0]['FILE']
  print(exp_id, file)
      
except Exception as e:
  print('got error: %s' % e)
finally:
  clean_temp_dir(temp_dir)

