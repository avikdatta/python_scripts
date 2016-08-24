import os,sys
import re
from collections import defaultdict
from json_hub import read_index_file,required_attributes,experiment_metadata,sample_metadata,analysis_metadata

file_type_key='FILE_TYPE'
exp_id_key='EXPERIMENT_ID'
epirr_id_key='EPIRR_ID'

index='/home/pi/python/pr7/work/test.index'
index_data=read_index_file(index,exp_id_key)
analysis_file='/home/pi/json_trackhub/trackhub/analysis_info.txt'
analysis_data=read_index_file(analysis_file,file_type_key)
epirr_index='/home/pi/json_trackhub/trackhub/epirr_20160818.index'
epirr_data=read_index_file(epirr_index,exp_id_key)


for exp,entries in index_data.items():
  sample_data=sample_metadata(entries[0])
  for experiment in entries:
    file_type=experiment[file_type_key]
    if file_type in analysis_data:          
      '''
      Skip if file type is not required for trackhub
      '''
      exp_meta=experiment_metadata(experiment)
      analysis_meta=analysis_metadata(analysis_data[file_type][0])
      epirr_id=epirr_data[exp][0][epirr_id_key]
      print(exp,epirr_id) 






