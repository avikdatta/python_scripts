import os,sys
import re
from collections import defaultdict
from json_hub import read_index_file,required_attributes,experiment_metadata,sample_metadata,analysis_metadata, file_dict

file_type_key='FILE_TYPE'
exp_id_key='EXPERIMENT_ID'
epirr_id_key='EPIRR_ID'
sample_id_key='SAMPLE_ID'
exp_id_key='EXPERIMENT_ID'
url_prefix='http://ftp.ebi.ac.uk/pub/databases/'

index='/home/pi/python/pr7/work/test.index'
index_data=read_index_file(index,exp_id_key)
analysis_file='/home/pi/json_trackhub/trackhub/analysis_info.txt'
analysis_data=read_index_file(analysis_file,file_type_key)
epirr_index='/home/pi/json_trackhub/trackhub/epirr_20160818.index'
epirr_data=read_index_file(epirr_index,exp_id_key)

samples_dict=defaultdict(dict)
dataset_dict=defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for exp,entries in index_data.items():
  sample_data=sample_metadata(entries[0])
  sample_id=entries[0][sample_id_key]
  samples_dict['samples'][sample_id]=sample_data
 
  for experiment in entries:
    file_type=experiment[file_type_key]
    exp_id=experiment[exp_id_key]
    if file_type in analysis_data:          
      '''
      Skip if file type is not required for trackhub
      '''
      exp_meta=experiment_metadata(experiment)
      analysis_meta=analysis_metadata(analysis_data[file_type][0])
      browser_dict=file_dict(experiment,url_prefix)
      exp_meta[epirr_id_key]=epirr_data[exp][0][epirr_id_key]

      dataset_dict['datasets'][exp_id]['analysis_attributes']=analysis_meta
      dataset_dict['datasets'][exp_id]['experiment_attribute']=exp_meta
      dataset_dict['datasets'][exp_id]['browser'].append(browser_dict)     

print(dataset_dict)


