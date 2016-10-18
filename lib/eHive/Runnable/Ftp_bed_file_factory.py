import eHive, os
import pandas as pd
from collection import defaultdict
from urllib.parse import urlsplit, urlunparse

class Ftp_bed_file_factory(eHive.BaseRunnable):

  def run(self):
    # fetch index file
    index_file=self.param_required('index_file')  
 
    # prepare list of seeds
    seed_list=read_index_data(index=index_file)

    # set seed list in param
    self.param('seed_list', seed_list)

  def write_output(self):
    seed_list=self.param('seed_list')
    self.dataflow(seed_list, 2)

  def read_index_data(index):
    '''
    This function accept an index file and prepare a list of seeds
    containing the experiment id and file url
    '''
    
    # define empty list of dict
    seed_list = defaultdict(lambda: dict)

    try:
      # read index file in chunks of 4000 lines
      data=pd.read_table(index_file, chunksize=4000)
      
      for data_chunk in data:
        chip_exps=data_chunk.groupby('LIBRARY_STRATEGY').get_group('ChIP-Seq').groupby('EXPERIMENT_ID').groups.keys()
        data_chunk=data_chunk.set_index('EXPERIMENT_ID')
        
        for exp_id in chip_exps:
          if type(data_chunk.loc[exp_id]['FILE']) is str:
            file_uri=data_chunk.loc[exp_id]['FILE']
          else:
            file_uri=data_chunk.loc[exp_id][data_chunk.loc[exp_id]['FILE'].str.contains('bed.gz')]['FILE'][exp_id]

          if not file_uri:
            raise Exception('No file uri found for exp id: {0}'.format(exp_id))

          if file_uri.endswith('bed.gz'):
            # Process only bed files
            file_uri=urlunparse(('http',ftp_url, dir_prefix + file_uri,'','',''))
            seed_list.append({'experiment_id':exp_id, 'file_uri':file_uri)      

    except Exception as e:
      self.warning('Got error: {0}'.format(e))

    return seed_list
