#!/usr/bin/env python3

import os
import pandas as pd

def get_data():
  #read a local file(todo)
  bindir = os.path.abspath(os.path.dirname(__file__))
  file=bindir+'/../../../data/20160816.data.index'
  file_path=os.path.abspath(file)

  #Read the index file as pandas DataFrame
  data=pd.read_table(file)
  return data

