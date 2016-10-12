#!/usr/bin/env python3

import os, argparse
import pandas as pd
from urllib.parse import urlsplit, urlunparse
from blueprint.stats.get_ftp_bed_files_stats import get_bed_file, get_bed_stats 


parser=argparse.ArgumentParser()
parser.add_argument('-w','--work_dir',required=True, help='Work directory')
parser.add_argument('-o','--output_csv',required=True, help='Output CVS file')
parser.add_argument('-i','--index_file',required=True, help='Index file')
parser.add_argument('-f','--ftp_url', default='ftp.ebi.ac.uk', help='FTP url, default: ftp.ebi.ac.uk')
parser.add_argument('-d','--dir_prefix', default='/pub/databases/', help='FTP directory prefix, default: /pub/databases/')
args=parser.parse_args()

ftp_url=args.ftp_url
dir_prefix=args.dir_prefix
index_file=args.index_file
work_dir=args.work_dir
output_csv=args.output_csv

data=pd.read_table(index_file)

# List ChIP-Seq experiments

chip_exps=data.groupby('LIBRARY_STRATEGY').get_group('ChIP-Seq').groupby('EXPERIMENT_ID').groups.keys()

# Set EXPERIMENT_ID as the index

data=data.set_index('EXPERIMENT_ID')
df=pd.DataFrame({})

df_header=[]

for exp_id in chip_exps:
  if type(data.loc[exp_id]['FILE']) is str:
    file_uri=data.loc[exp_id]['FILE']
  else:
    file_uri=data.loc[exp_id][data.loc[exp_id]['FILE'].str.contains('bed.gz')]['FILE'][exp_id]
  if file_uri.endswith('bed.gz'):
    df_header.append(exp_id)
    file_uri=urlunparse(('http',ftp_url, dir_prefix + file_uri,'','',''))
    url=urlsplit(file_uri)
    (dir_path, file_path)=os.path.split(url.path)
    (data_list, output_png)=get_bed_stats(work_dir=work_dir,ftp_url=url.netloc, dir=dir_path, file=file_path, prefix=exp_id)

    if df.empty:
      df=pd.DataFrame(data_list)
      df=df.set_index('chr')
    else:
      next_df=pd.DataFrame(data_list)
      next_df=next_df.set_index('chr')

      # Concatenate dataframe for each BED file
      df=pd.concat([df, next_df], join='outer', axis=1)

df.columns=df_header

# Write DataFrame to output CSV
df.to_csv(output_csv, sep='\t')  

