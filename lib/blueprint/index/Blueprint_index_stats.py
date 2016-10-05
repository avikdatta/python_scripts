#!/usr/bin/env python3

import os
import pandas as pd
from collections import defaultdict

#Preparea a group of assays

def get_counts(data):
  assay_group=data.groupby('LIBRARY_STRATEGY')
  assay_count_dict=defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

  #Get counts of assays and histone marks
 
  for assay_name in assay_group.groups.keys():
    assay_data=assay_group.get_group(assay_name)
    assay_count=len(assay_data.groupby('EXPERIMENT_ID').groups.keys())
    assay_count_dict[assay_name]['EXPERIMENT_COUNT']=assay_count
    bio_type_group=assay_data.groupby('BIOMATERIAL_TYPE')

    #Get biomaterial type groups per assay
    for bio_type in bio_type_group.groups.keys():
      bio_type_data=bio_type_group.get_group(bio_type)
      bio_type_count=len(bio_type_data.groupby('EXPERIMENT_ID').groups.keys())
      assay_count_dict[assay_name][bio_type]['EXPERIMENT_COUNT']=bio_type_count

      #Count cell types per assays
      if bio_type == 'Primary Cell':
        cell_type_group=bio_type_data.groupby('CELL_TYPE')
      
        #Count experiments for each cell type
        for cell_type in cell_type_group.groups.keys():
          cell_type_data=cell_type_group.get_group(cell_type)
          cell_type_count=len(cell_type_data.groupby('EXPERIMENT_ID').groups.keys())
          assay_count_dict[assay_name][bio_type][cell_type]=cell_type_count

    if assay_name == 'ChIP-Seq':
      chip_group=assay_data.groupby('EXPERIMENT_TYPE')
      for histone in chip_group.groups.keys():
        histone_data=chip_group.get_group(histone)
        histone_count=len(histone_data.groupby('EXPERIMENT_ID').groups.keys())
        assay_count_dict[assay_name]['HISTONE'][histone]=histone_count

  return assay_count_dict

