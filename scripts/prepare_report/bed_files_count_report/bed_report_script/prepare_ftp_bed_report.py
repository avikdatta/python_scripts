#!/usr/bin/env python3

import argparse
from blueprint.stats.get_ftp_bed_files_stats import generate_bed_stats_from_index

parser=argparse.ArgumentParser()
parser.add_argument('-w','--work_dir',required=True, help='Work directory')
parser.add_argument('-f','--ftp_url', default='ftp.ebi.ac.uk', help='FTP host, default: ftp.ebi.ac.uk')
parser.add_argument('-d','--ftp_dir', default='/pub/databases/', help='FTP directory path, default: /pub/databases/')
parser.add_argument('-i','--index_file', required=True, help='Index file contataining the bed file path')
parser.add_argument('-e', '--id', required=True, help='Experiment id for ChIp-Seq data')
args=parser.parse_args()

work_dir   = args.work_dir
ftp_url    = args.ftp_url
dir_prefix = args.ftp_dir
index      = args.index_file
exp_id     = args.id


(data_file, output_plot)=generate_bed_stats_from_index(index=index, exp_id=exp_id, ftp_url=ftp_url, dir_prefix=dir_prefix, work_dir=work_dir)

print(data_file)
print("Generated png plot: %s" % output_plot)
