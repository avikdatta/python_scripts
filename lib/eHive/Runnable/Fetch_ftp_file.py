import eHive, os, sys
from shutil import move
from urllib.parse import urlsplit
from blueprint.stats.get_ftp_bed_files_stats import get_temp_dir, get_ftp_file, clean_temp_dir

class Fetch_ftp_file(eHive.BaseRunnable):

  def fetch_input(self):
    file_uri=self.param_required('file_uri')
    url=urlsplit(file_uri)
    (ftp_dir_path, ftp_file_path)=os.path.split(url.path)    

    # set params
    self.param('ftp_url')=url.netloc
    self.param('ftp_dir_path', ftp_dir_path)
    self.param('ftp_file_path', ftp_file_path)

  def run(self):
    experiment_id=self.param_required('experiment_id')
    store_dir=self.param_required('store_dir')    

    ftp_dir_path=self.param('ftp_dir_path')
    ftp_file_path=self.param('ftp_file_path')
    ftp_url=self.param('ftp_url')
 
    output_file_path=os.path.join(store_dir, ftp_file_path)
    
    temp_dir=get_temp_dir(store_dir)
    temp_file=os.path.join(temp_dir, ftp_file_path)
    cwd=os.getcwd()

    try:
      os.chdir(temp_dir)
      get_ftp_file(ftp_url=ftp_url, dir=ftp_dir_path, file=ftp_file_path)
    except Exception as e:
      self.warning('failed to download file: {0}, error: {1}'.format(ftp_file_path,e))   
      sys.exit(2)
    else:
      move(temp_file, output_file_path)
      self.param('output_file_path', output_file_path)
    finally:
      os.chdir(cwd)
      clean_temp_dir(temp_dir)
    
  def  write_output(self):
    self.dataflow( { 'output_file_path' : self.param('output_file_path') }, 1)


