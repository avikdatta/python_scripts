import os
from collections import defaultdict, deque

class SampleSheet:
  def __init__(self, infile, data_header_name='Data'):
    self.infile=infile 
    self.data_header_name=data_header_name 

  def filter_sample_data( self, condition_key, condition_val ):
    self._sample_data=self._read_samplesheet()
    header_data=self._load_header()
    data_header, raw_data=self._load_data()
    filtered_data=list()

    for row in raw_data:
      if condition_key not in list(row.keys()): 
        raise ValueError('key {} not found for {}'.format(condition_key, row))
      else:
        if row[condition_key] == condition_val: filtered_data.append(row)

    # formatting output
    for header_key in header_data.keys():
      print('[{}]'.format(header_key))
      for row in header_data[header_key]:
         print(row)

    print('[{}]'.format(self.data_header_name))
    print(','.join(data_header))

    for row in filtered_data:
      data_row=list()
      for h in data_header:
        data_row.append(row[h])
      print(','.join(data_row))

  def _load_header(self):
    sample_data=self._sample_data
    header_data=dict()

    for keys in sample_data:
      if keys != self.data_header_name: 
        header_data[keys]=sample_data[keys]   
    return header_data
  
  def _load_data(self):
    sample_data=self._sample_data
    data=sample_data[self.data_header_name]
    data=deque(data)
    data_header=data.popleft()
    data_header=data_header.split(',')
    sample_data=list()
    for row in data:
      row=row.split(',')
      row_data=dict(zip(data_header,row))
      sample_data.append(row_data)
    #print(data_header)
    return data_header, sample_data
  
  def _read_samplesheet(self):
    infile=self.infile

    if os.path.exists(infile) == False:
      raise IOError('file {0} not found'.format(infile))

    sample_data=defaultdict(list)
    header=''

    with open(infile, 'r') as f:
      for i in f:
        row=i.rstrip('\n')
        if row.startswith('['):
           header=row.strip('[').strip(']')
        else:
           sample_data[header].append(row)
    return sample_data
