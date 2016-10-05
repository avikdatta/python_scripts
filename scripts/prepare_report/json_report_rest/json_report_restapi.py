#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource
from blueprint.data.Blueprint_local_data import get_data
from blueprint.index.Blueprint_index_stats import get_counts

app=Flask(__name__)
api=Api(app)

data=get_data()

class Json_report(Resource):
  def get(self):
    return get_counts(data)

api.add_resource(Json_report,'/json_stats')

if __name__=='__main__':
  app.run(debug=True)

