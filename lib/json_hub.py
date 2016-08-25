import os,sys
import re
from collections import defaultdict

def file_dict(experiment,url_prefix):
  file_name=os.path.basename(experiment['FILE'])
  lib_strategy=experiment['LIBRARY_STRATEGY']

  if file_name.endswith('bw'):
    if re.match(r'plusStrand', file_name, re.IGNORECASE):
      type='signal_forward'
    elif re.match(r'minusStrand', file_name, re.IGNORECASE):
      type='signal_reverse'
    else:
      type='signal_unstranded'
  elif file_name.endswith('bb'):
      type='peak_calls'
  else:
      type='other'

  file_url = url_prefix + experiment['FILE']
  browser_dict = defaultdict(dict)
  browser_dict['big_data_url']=file_url
  browser_dict['md5sum']=experiment['FILE_MD5']
  browser_dict['primary']=True
  return browser_dict,type

def read_index_file(infile, key_text):
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
    file_list=defaultdict(list)
    for i in f:
      row=i.rstrip('\n').split("\t")
      if(header):
        filtered_dict=dict(zip(header,row))
        exp_id=filtered_dict[key_text]
        file_list[exp_id].append(filtered_dict)
      else:
        header=map(str.upper, row)
        if key_text not in header:
          print('key %s not found in file %s' % (key_text, index))
          sys.exit(2)
  return file_list

def required_attributes(type):
  donor=['DONOR_ID', 'DONOR_AGE', 'DONOR_AGE_UNIT', 'DONOR_LIFE_STAGE',
         'DONOR_HEALTH_STATUS', 'DONOR_SEX', 'DONOR_ETHNICITY',
        ]
  meta= ['SAMPLE_ONTOLOGY_URI', 'MOLECULE', 'DISEASE', 'DISEASE_ONTOLOGY_URI', 'BIOMATERIAL_TYPE']

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
  list.extend(meta)
  return list

def analysis_metadata(analysis):
  required=['ANALYSIS_GROUP','ALIGNMENT_SOFTWARE','ALIGNMENT_SOFTWARE_VERSION','ANALYSIS_SOFTWARE','ANALYSIS_SOFTWARE_VERSION'] 
  analysis_dict=dict((k.lower(),v) for k,v in analysis.items() if k in required)
  return analysis_dict

def experiment_metadata(experiment):
  required=['EXPERIMENT_TYPE','EXPERIMENT_ONTOLOGY_URI','REFERENCE_REGISTRY_ID']
  exp_dict=dict((k.lower(),v) for k,v in experiment.items() if k in required)
  exp_dict['experiment_ontology_uri']='-'
  exp_dict['assay']=experiment['LIBRARY_STRATEGY']
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
  sample_dict=dict((k.lower(),v) for k,v in sample.items() if k in required)

  # JSON hub validator doesn't allow space in the age
  if 'donor_age' in sample_dict:
    sample_dict['donor_age']=re.sub(r'\s+','',sample_dict['donor_age'])

  sample_dict['donor_life_stage']='unknown'
  sample_dict['donor_age_unit']='year'
  return sample_dict

