import os,sys,re, json
from collections import defaultdict
from json_hub import read_index_file,required_attributes,experiment_metadata,sample_metadata,analysis_metadata, file_dict

file_type_key = 'FILE_TYPE'
file_key      = 'FILE'
exp_id_key    = 'EXPERIMENT_ID'
epirr_id_key  = 'EPIRR_ID'
sample_id_key = 'SAMPLE_ID'
exp_id_key    = 'EXPERIMENT_ID'
url_prefix    = 'http://ftp.ebi.ac.uk/pub/databases/'

index='/nfs/1000g-work/ihec/work/bp_pipe/dcc_work/2016/08_16/25_08_16/json_hub/public.results_GRCh38.index'
index_data=read_index_file(index,exp_id_key)
analysis_file='/nfs/1000g-work/ihec/work/bp_pipe/dcc_work/2016/08_16/25_08_16/json_hub/analysis_info.txt'
analysis_data=read_index_file(analysis_file,file_type_key)
epirr_index='/nfs/1000g-work/ihec/work/bp_pipe/dcc_work/2016/08_16/25_08_16/json_hub/epirr_20160818.index'
epirr_data=read_index_file(epirr_index,exp_id_key)


hub_dict={
    "assembly": "hg38", 
    "date": "2016-08-16", 
    "description": "Blueprint JSON Data hub generated for the IHEC Data Portal.", 
    "email": "blueprint-info@ebi.ac.uk", 
    "publishing_group": "Blueprint", 
    "releasing_group": "Blueprint", 
    "taxon_id": 9606
   }

samples_dict=defaultdict(dict)
dataset_dict=defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for exp,entries in index_data.items():
  sample_data=sample_metadata(entries[0])
  sample_id=entries[0][sample_id_key]
  samples_dict[sample_id]=sample_data
 
  for experiment in entries:
    file_type=experiment[file_type_key]
    file_name=os.path.basename(experiment[file_key])
    exp_id=experiment[exp_id_key]
    if re.match(r'\.(bb|bw)$',file_name):
   # if file_type in analysis_data:          
      '''
      Skip if file type is not required for trackhub
      '''
      exp_meta=experiment_metadata(experiment)
      analysis_meta=analysis_metadata(analysis_data[file_type][0])
      (browser_dict,type)=file_dict(experiment,url_prefix)
      exp_meta[epirr_id_key]=epirr_data[exp][0][epirr_id_key]
      
      dataset_dict[exp_id]['analysis_attributes']=analysis_meta
      dataset_dict[exp_id]['experiment_attributes']=exp_meta
      dataset_dict[exp_id]['browser'][type].append(browser_dict) 
      dataset_dict[exp_id]['sample_id']=sample_id    

json_obj={ 'hub_description': hub_dict, 'datasets': dataset_dict, 'samples': samples_dict}
print json.dumps(json_obj,indent=4)


