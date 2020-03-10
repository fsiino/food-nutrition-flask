# Food Nutrition App

Taking this opportunity to familiarize myself with Python + Flask.

First version with Express backend: <a href="https://github.com/fsiino/food-nutrition-express" target="_blank">https://github.com/fsiino/food-nutrition-express</a>

### Live Link
<a href="https://protected-woodland-23217.herokuapp.com/" target="_blank">https://protected-woodland-23217.herokuapp.com/</a>

<img src="https://github.com/fsiino/food-nutrition-flask/blob/master/docs/fn-main.png?raw=true" alt="Screenshot">

## Objective
Create a backend Rest API with an endpoint URL called by the user to find foods containing nutrients within a specified range in grams. Serve the data over a frontend framework with a user-friendly search interface.

## Technologies
* MongoDB
* Flask
* React
* PyMongo
* Axios

## Screen GIFs
### Search 
<img src="https://github.com/fsiino/food-nutrition-express/blob/master/docs/fn-search.gif?raw=true" alt="search">

### Fieldset Buttons
<img src="https://github.com/fsiino/food-nutrition-express/blob/master/docs/fn-buttons.gif?raw=true" alt="buttons">

## Code Snippets

```js
// client/components/Form.jsx
  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    let query = '';
    const fieldsetsCopy = fieldsets;
    let inputNutrients = '';
    let inputMins = '';
    let inputMaxes = '';
    for (let i = 0; i < fieldsetsCopy.length; i++) {
      const fieldsetCopy = fieldsetsCopy[i];
      const nutrient = fieldsetCopy.nutrient.toLowerCase();
      let min = fieldsetCopy.min;
      let max = fieldsetCopy.max;
      if (!nutrient || (nutrient.includes(','))) continue;
      if (!min) min = 0;
      if (!max) max = 99999; 
      inputNutrients += `${nutrient},`;
      inputMins += `${min},`;
      inputMaxes += `${max},`;
    }  
    query += `nutrients=${inputNutrients.slice(0, inputNutrients.length-1)}&mins=${inputMins.slice(0, inputMins.length-1)}&maxes=${inputMaxes.slice(0, inputMaxes.length-1)}`
    axios.get(`/api/foods/search?${query}`)
      .then(res => {
        if (res.data.length > 0) {
          setResults(res.data);
          setLoading(false);
        } else {
          // ...
  };
```
Originally, each `nutrient`, `min`, and `max` row `fieldset` was a separate GET request whose result(s) were concatenated and updated in the `Form` component's local state to be displayed. Because this proved to be inefficient and less scalable, the backend routes were revised to allow chained search parameters in a single search. The frontend `handleSubmit` function was then rewritten accordingly, taking the axios calls out of the loop and instead making a single call with a finalized url.

```py
# app.py
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
      'nutrients': { '$elemMatch': { 'nutrient': {"$regex": regex, "$options": "-i"}, 'gm': { '$gt': int(fieldsets[1][i]), '$lte': int(fieldsets[2][i]) } } }
    }
    queries.append(query)

  results = food.find({'$and' : queries})
  return json_util.dumps(results, default=json_util.default)
```
Each time a user performs a search, the data is fetched on the backend using the `/search` route. On the frontend, parameters are concatenated into comma-separated strings before being added to the url. Once the request is received on the backend, a `.split(',')` is performed on the strings depending on how many fieldsets the user added to their search query, and sent to MongoDB for retrieval.

