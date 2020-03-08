from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

import config
from bson import json_util

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = config.api_key

mongo = PyMongo(app)

@app.route('/api/foods/all', methods=['GET'])
def get_all_foods():
  food = mongo.db.foods
  output = []
  for food in food.find():
    output.append({'ndbno': food['ndbno'], 'name': food['name'], 'weight': food['weight'],
                   'measure': food['measure'], 'nutruents': food['nutrients']})
  return jsonify({'result': output})

@app.route('/api/foods/search', methods=['GET'])
def get_queried_foods():
  food = mongo.db.foods
  fieldsets = []
  results = []
  queries = []

  nutrients = request.args.get('nutrients').split(',')
  mins = request.args.get('mins').split(',')
  maxes = request.args.get('maxes').split(',')

  fieldsets.append(nutrients)
  fieldsets.append(mins)
  fieldsets.append(maxes)

  for i in range(len(fieldsets)-1):
    query = {
      'nutrients': {
        '$elemMatch': {
          'nutrient': fieldsets[0][i],
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
