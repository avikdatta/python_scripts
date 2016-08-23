import os,sys
import re

def read_index_file(infile, f_header=[]):
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

index='/home/pi/python/pr7/work/test.index'
index_dict=read_index_file(index)

for exp,entries in index_dict.items():
  bio_type=entries[0]['BIOMATERIAL_TYPE']
  if re.match(r'\bprimary\scell\b', bio_type, re.IGNORECASE):
    print('%s %s' % (exp,bio_type)) 
  elif re.match(r'\bprimary\stissue\b', bio_type, re.IGNORECASE):
    print('%s\t%s' % (exp,bio_type))
  elif re.match(r'\bcell\sline\b', bio_type, re.IGNORECASE):
    print('%s\t%s' % (exp,bio_type))
  elif re.match(r'\bprimary\scell\sculture\b', bio_type, re.IGNORECASE):
    print('%s\t%s' % (exp,bio_type))
  else:
    print('Unknown type: %s' % bio_type)
