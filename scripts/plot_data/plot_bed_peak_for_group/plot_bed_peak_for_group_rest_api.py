#!/usr/bin/env python3

import os, argparse
import pandas as pd
from flask import Flask, make_response, send_file
from flask_restful import Api, Resource, reqparse, abort
from blueprint.stats.plot_bed_peak_counts import groupby_histone, plot_box_chart
from ftp_index_method import get_temp_dir, clean_temp_dir


parser=argparse.ArgumentParser()
parser.add_argument('-w','--work_dir',required=True, help='Work directory')
parser.add_argument('-i','--index_file', required=True, help='Index file contataining the bed file path')
parser.add_argument('-d','--csv_data', required=True, help='CSV dataframe containing BED peak counts per chromosome')
parser.add_argument('-p','--host', default='127.0.0.1', help='REST api host ip')
args=parser.parse_args()

work_dir   = args.work_dir
index_file = args.index_file
csv_data   = args.csv_data
host       = args.host

app=Flask(__name__)
api=Api(app)

chrs=['chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22']

allowed_histone=['H3K4me1', 'H2A.Zac', 'H3K27me3',  'H3K9/14ac', 'H3K9me3', 'H3K4me3',  'H3K27ac', 'H3K36me3']

peak_data=pd.read_table(csv_data)
peak_data=peak_data.set_index('chr')
peak_data=peak_data.fillna(0)

index_data=pd.read_table(index_file)

@api.representation('image/png')
def output_png(file, code, headers=None):
  resp = make_response(file,code)
  return send_file(file)


class Plot_histone(Resource):
  '''
  Plot peak count for specific histone mark
  '''
  def get(self):
    h_parser=reqparse.RequestParser()
    h_parser.add_argument('histone', required=True, help='Histone mark name')
    h_parser.add_argument('chr', default=chrs, action='append', help='Lists of chromosomes')
    h_args=h_parser.parse_args()
    
    chr_list=h_args['chr']
    histone=h_args['histone']
  
    if histone in allowed_histone:
      try:
        histone_exps=groupby_histone(dataframe=index_data, histone=histone)
        temp_dir=get_temp_dir(work_dir=work_dir)
        os.chdir(temp_dir)
        filename=histone+'.png'
        filename=os.path.join(temp_dir,filename)
        plot_box_chart(dataframe=peak_data[histone_exps].T, filename=filename, chr_list=chrs)
        return output_png(file=filename,code=201)
      except Exception as e:
        abort(404, message='got error')
      finally:
        clean_temp_dir(temp_dir)
    else:
      abort(404,message='unsupported histone name: {0}'.format(histone))

class Plot_all_data(Resource):
  '''
  Plot peak count for all histone marks
  '''
  def get(self):
    h_parser=reqparse.RequestParser()
    h_parser.add_argument('chr', default=chrs, action='append', help='Lists of chromosomes')
    h_args=h_parser.parse_args()

    chr_list=h_args['chr']

    try:
      temp_dir=get_temp_dir(work_dir=work_dir)
      os.chdir(temp_dir)
      filename='all_histone.png'
      filename=os.path.join(temp_dir,filename)
      plot_box_chart(dataframe=peak_data.T, filename=filename, chr_list=chrs)
      return output_png(file=filename,code=201)
    except Exception as e:
      abort(404, message='got error')
    finally:
      clean_temp_dir(temp_dir)

      

    
api.add_resource(Plot_histone, '/histone_peak')
api.add_resource(Plot_all_data, '/all_histone')

if __name__=='__main__':
  app.run(host=host)

