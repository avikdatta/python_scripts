#!/usr/bin/env python3

import argparse, json
from flask import Flask, make_response, send_file
from flask_restful import Api, Resource, reqparse, abort
from blueprint.stats.get_ftp_bed_files_stats import generate_bed_stats_from_index

parser=argparse.ArgumentParser()
parser.add_argument('-w','--work_dir',required=True, help='Work directory')
parser.add_argument('-f','--ftp_url', default='ftp.ebi.ac.uk', help='FTP host, default: ftp.ebi.ac.uk')
parser.add_argument('-d','--ftp_dir', default='/pub/databases/', help='FTP directory path, default: /pub/databases/')
parser.add_argument('-i','--index_file', required=True, help='Index file contataining the bed file path')
parser.add_argument('-p','--host', default='127.0.0.1', help='REST api host ip')
args=parser.parse_args()


work_dir   = args.work_dir
ftp_url    = args.ftp_url
dir_prefix = args.ftp_dir
index      = args.index_file
host       = args.host

app=Flask(__name__)
api=Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
  resp = make_response(json.dumps(data),code)
  resp.headers.extend(headers or {})
  return resp

@api.representation('image/png')
def output_png(data, code, headers=None):
  resp = make_response(data,code)
  return send_file(data)

class Json_report_and_plot(Resource):
  def get(self):
    f_parser=reqparse.RequestParser()
    f_parser.add_argument('exp_id', required=True, help='Experiment id')
    f_parser.add_argument('mode', default='json', help='Output format, either json or png')
    f_args  = f_parser.parse_args()

    exp_id  = f_args['exp_id']
    mode    = f_args['mode']

    (json_data, output_plot)=generate_bed_stats_from_index(index=index, exp_id=exp_id, ftp_url=ftp_url, dir_prefix=dir_prefix, work_dir=work_dir)

    if mode == 'json':
      output=output_json(json_data,201)
    elif mode == 'png':
      output=output_png(output_plot, 201)
    else:
      abort(404,message='unsupported format {0}'.format(mode))

    return output

api.add_resource(Json_report_and_plot, '/bed_stats')

if __name__=='__main__':
  app.run(host=host)
