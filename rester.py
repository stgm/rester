from collections import defaultdict
from flask import Flask, request
from flask_restful import abort, Api, Resource

app = Flask(__name__)
api = Api(app)

DATA = defaultdict(list)

DATA['categories'] = {
    "categories": [
        "appetizers",
        "entrees"
    ]
}

DATA['menu'] = [
    {
        "id": 1,
        "name": "Spaghetti and Meatballs",
        "description": "Seasoned meatballs on top of freshly-made spaghetti. Served with a robust tomato sauce.",
        "price": 9.0,
        "category": "entrees",
        "imageName": "spaghetti.jpg"
    },
    {
        "id": 2,
        "name": "Margherita Pizza",
        "description": "Tomato sauce, fresh mozzarella, basil, and extra-virgin olive oil.",
        "price": 10.0,
        "category": "entrees",
        "imageName": "pizza.jpg"
    },
    {
        "id": 3,
        "name": "Grilled Steelhead Trout Sandwich",
        "description": "Pacific steelhead trout* with lettuce, tomato, and red onion.",
        "price": 9.0,
        "category": "entrees",
        "imageName": "trout.jpg"
    },
    {
        "id": 4,
        "name": "Pesto Linguini",
        "description": "Stewed sliced beef with yellow onions and garlic in a vinegar-soy sauce. Served with steamed jasmine rice and sautéed vegetables.",
        "price": 9.0,
        "category": "entrees",
        "imageName": "pesto.jpeg"
    },
    {
        "id": 5,
        "name": "Chicken Noodle Soup",
        "description": "Delicious chicken simmered alongside yellow onions, carrots, celery, and bay leaves, chicken stock.",
        "price": 3.0,
        "category": "appetizers",
        "imageName": "chickensoup.jpg"
    },
    {
        "id": 6,
        "name": "Italian Salad",
        "description": "Garlic, red onions, tomatoes, mushrooms, and olives on top of romaine lettuce.",
        "price": 5.0,
        "category": "appetizers",
        "imageName": "italiansalad.jpg"
    }
]

# what comes from this is quite ambiguous: a dict with a message item
# it's fairly indistinguishable from a real item
def abort_item(list_id, item_id):
    abort(404, message=f"Item {item_id} doesn't exist in list {list_id}")

# parser = reqparse.RequestParser()
# parser.add_argument('task')

# find items in a list based on some attribute's value
def query(data, key, value):
    results = filter(lambda item: item[key] == value, data)
    return results

# find first item in a list that has item_id
def find(data, item_id):
    results = query(data, 'id', item_id)
    try:
        # return first item if possible
        return next(results)
    except StopIteration:
        raise LookupError

def remove(data, item_id):
    results = list(filter(lambda item: item['id'] != item_id, data))
    return results    

def max_id(data):
    ids = list(map(lambda item: item['id'], data))
    if len(ids) == 0:
        return 0
    else:
        return max(ids)


class Item(Resource):

    def get(self, list_id, item_id):
        try:
            return find(DATA[list_id], int(item_id))
        except LookupError:
            abort_item(list_id, item_id)

    def delete(self, list_id, item_id):
        DATA[list_id] = remove(DATA[list_id], int(item_id))
        return '', 204

    def put(self, list_id, item_id):
        try:
            item = find(DATA[list_id], int(item_id))
        except LookupError:
            abort_item(list_id, item_id)
        other = remove(DATA[list_id], int(item_id))
        item.update(request.form.to_dict(flat=True))
        DATA[list_id] = other + [item]
        return DATA[list_id], 201


class List(Resource):

    def get(self, list_id):
        return DATA[list_id]

    def post(self, list_id):
        # get previous max id and add 1
        item_id = max_id(DATA[list_id]) + 1
        # create item and add all POSTed arguments
        item = { 'id': item_id, **request.form.to_dict(flat=True) }
        DATA[list_id].append(item)
        return item, 201

##
## Setup the API resource routing
##
api.add_resource(Item, '/<list_id>/<item_id>')
api.add_resource(List, '/<list_id>')


if __name__ == '__main__':
    app.run(debug=True)
