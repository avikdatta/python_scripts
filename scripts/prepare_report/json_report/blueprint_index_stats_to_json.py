#!/usr/bin/env python3

import pandas as pd
import os, json, argparse
from blueprint.index.Blueprint_index_stats import get_counts

parser=argparse.ArgumentParser()
parser.add_argument('-i','--infile', required=True, help='Input index file')
args=parser.parse_args()

file=args.infile
file_path=os.path.abspath(file)

#Read the index file as pandas DataFrame
data=pd.read_table(file)

#Preparea a group of assays
assay_count_dict=get_counts(data)

#Print JSON report for all assays
print(json.dumps(assay_count_dict,indent=4))
