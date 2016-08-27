import os,sys
import re
from collections import defaultdict

class Ihec_json_hub:
  def __init__(self, **data):
    self.hub_description = data['hub_description']


  def get_json_data(self):
    '''
    add project specific method
    '''
    dataset_dict={}
    sample_dict={}
    return dataset_dict,sample_dict
 

  def json_hub(self,dataset_data, sample_data):
    '''
    IHEC JSON structure
    '''
    json_obj={ 'hub_description': hub_dict, 
               'datasets': dataset_dict, 
               'samples': samples_dict
             }
    return json_obj
    
