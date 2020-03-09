from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

import config
from bson import json_util
import re

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = config.api_key

mongo = PyMongo(app)

@app.route('/api/foods/all', methods=['GET'])
def get_all_foods():
  food = mongo.db.foods
  output = []
  for food in food.find():
    output.append({'ndbno': food['ndbno'], 'name': food['name'], 'weight': food['weight'],
                   'measure': food['measure'], 'nutrients': food['nutrients']})
  return jsonify(output)

@app.route('/api/foods/search', methods=['GET'])
def get_queried_foods():
  food = mongo.db.foods
  fieldsets = []
  results = []
  queries = []

  nutrients_params = request.args.get('nutrients')
  mins_params = request.args.get('mins')
  maxes_params = request.args.get('maxes')

  if ',' in nutrients_params:
    nutrients = nutrients_params.split(',')
  else:
    nutrientsList = []
    nutrientsList.append(nutrients_params)
    nutrients = nutrientsList

  if ',' in mins_params:
    mins = mins_params.split(',')
  else:
    minsList = []
    minsList.append(mins_params)
    mins = minsList

  if ',' in maxes_params:
    maxes = maxes_params.split(',')
  else:
    maxesList = []
    maxesList.append(maxes_params)
    maxes = maxesList

  fieldsets.append(nutrients)
  fieldsets.append(mins)
  fieldsets.append(maxes)

  for i in range(len(fieldsets[0])):
    regex = ".*" + fieldsets[0][i] + ".*"
    query = {
      'nutrients': {
        '$elemMatch': {
          'nutrient': {"$regex": regex, "$options": "-i"},
          'gm': {
            '$gt': int(fieldsets[1][i]),
            '$lte': int(fieldsets[2][i]),
          }
        }
      }
    }
    queries.append(query)

  results = food.find({'$and' : queries})
  return json_util.dumps(results, default=json_util.default)

@app.route('/')
def index():
  return jsonify({'msg': 'hello world'})

if __name__ == '__main__':
    app.run(debug=True)

# Run server in watch mode:
# FLASK_APP=app.py FLASK_ENV=development flask run --port=8000
