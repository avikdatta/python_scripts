import os,sys
import re
from collections import defaultdict

def read_index_file(infile ):
  '''
     Read an index file and a list of fields (optional)
     Returns a list of dictionary
  '''

  infile=os.path.abspath(infile)

  if os.path.exists(infile) == False:
    print('%s not found' % infile)
    sys.exit(2)

  with open(infile, 'r') as f:
    header=[]
    file_list={}
    for i in f:
      row=i.split("\t")
      if(header):
        filtered_dict=dict(zip(header,row))
        exp_id=filtered_dict['EXPERIMENT_ID']
        if exp_id not in file_list.keys():
          file_list[exp_id]=[]
        file_list[exp_id].append(filtered_dict)
      else:
        header=row
  return file_list

def required_attributes(type):
  donor=['DONOR_ID', 'DONOR_AGE', 'DONOR_AGE_UNIT', 'DONOR_LIFE_STAGE','DONOR_HEALTH_STATUS', 'DONOR_SEX', 'DONOR_ETHNICITY']
  required={ 'CELL_LINE' :['BIOMATERIAL_TYPE','LINE','LINEAGE','DIFFERENTIATION_STAGE','MEDIUM','SEX'],
             'PRIMARY_CELL': ['BIOMATERIAL_TYPE', 'CELL_TYPE'],
             'PRIMARY_TISSUE': ['BIOMATERIAL_TYPE','TISSUE_TYPE','TISSUE_DEPOT'],
             'PRIMARY_CELL_CULTURE':['BIOMATERIAL_TYPE', 'CELL_TYPE', 'CULTURE_CONDITIONS']
           }
  list=[]
  if type not in ['CELL_LINE',]:
    list=required[type]
    list.extend(donor)
  else:
    list=required[type]
  return list

 
def experiment_metadata(experiment):
  required=['EXPERIMENT_TYPE','LIBRARY_STRATEGY','EXPERIMENT_ONTOLOGY_URI','REFERENCE_REGISTRY_ID']
  exp_dict=dict((k,v) for k,v in experiment.items() if k in required)
  exp_dict['EXPERIMENT_ONTOLOGY_URI']='-'
  return exp_dict

def sample_metadata(sample):
  bio_type=sample['BIOMATERIAL_TYPE']
  if re.match(r'\bprimary\scell\b', bio_type, re.IGNORECASE):
    type='PRIMARY_CELL'
  elif re.match(r'\bprimary\stissue\b', bio_type, re.IGNORECASE):
    type='PRIMARY_TISSUE'
  elif re.match(r'cell\sline', bio_type, re.IGNORECASE):
    type='CELL_LINE'
  elif re.match(r'\bprimary\scell\sculture\b', bio_type, re.IGNORECASE):
    type='PRIMARY_CELL_CULTURE'
  else:
    print('Unknown type: %s' % bio_type)
    sys.exit(2)
  required=required_attributes(type)
  sample_dict=dict((k,v) for k,v in sample.items() if k in required)
  return sample_dict

index='/home/pi/python/pr7/work/test.index'
index_dict=read_index_file(index)
analysis_file''
epirr_index=''

for exp,entries in index_dict.items():
  sample_dict=sample_metadata(entries[0])
  print(sample_dict)
  for experiment in entries:
    exp_meta=experiment_metadata(experiment)
    print(exp_meta)






