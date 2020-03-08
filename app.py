from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

import config

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
  queries = []
  fieldsets.append(request.args)
  for el in fieldsets:
    query = {
      'nutrients': {
        '$elemMatch': {
          'nutrient': el['nutrient'],
          'gm': {
            '$gt': el['min'],
            '$lte': el['max']
          }
        }
      }
    }
    queries.append(query)

  # return jsonify({'fieldsets': fieldsets}, {'queries': queries})
  # print(queries)
  results = food.find({'$and' : queries})
  return jsonify({'results' : results})
  # # return jsonify({'queries' : queries})

@app.route('/')
def index():
  return jsonify({'msg': 'hello world'})

if __name__ == '__main__':
    app.run(debug=True)

# Run server in watch mode:
# FLASK_APP=app.py FLASK_ENV=development flask run --port=8000
