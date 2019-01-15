from collections import defaultdict
from flask import Flask, request, g
from flask_restful import abort, Api, Resource

app = Flask(__name__)
api = Api(app)

from database import *

if not os.path.exists(DATABASE):
    init_db(app)

@app.teardown_appcontext
def close_connection(exception):
    close_db()

def abort_item(list_id, item_id):
    abort(404, message=f"Item {item_id} doesn't exist in list {list_id}")


class Item(Resource):

    def get(self, list_id, item_id):
        
        data = query_db("select data from data where list = ? and item_id = ?", [list_id, item_id], one=True)
        
        if data is None:
            abort_item(list_id, item_id)
        else:
            # create json to return, includes item id
            item = { 'id': item_id, **json.loads(data['data']) }
            return item


    def delete(self, list_id, item_id):

        perform_db("delete from data where list = ? and item_id = ?", [list_id, item_id])
        return {}, 204


    def put(self, list_id, item_id):

        # TODO use transaction

        data = query_db("select data from data where list = ? and item_id = ?", [list_id, item_id], one=True)
        
        if data is None:
            abort_item(list_id, item_id)
        else:
            # merge old data with new (new overwrites any old keys)
            item_data = json.loads(data['data'])
            item_data.update(request.form.to_dict(flat=True))
            
            # save to database
            perform_db("update data set data = ? where list = ? and item_id = ?",
                [json.dumps(item_data), list_id, item_id])
            
            # create json to return, includes item id
            item = { 'id': item_id, **item_data }
            return item, 201


class List(Resource):

    def get(self, list_id):

        # get all items in this list
        data = query_db("select item_id, data from data where list = ?", [list_id])
        objects = [ { "id": item['item_id'], **json.loads(item['data']) } for item in data ]
        
        search = request.args
        
        # in json, show with id in each item
        if search:
            return [ obj for obj in objects if all([ nm in obj and obj[nm] == vl for nm,vl in list(search.items()) ]) ]
        else:
            return objects


    def post(self, list_id):

        # TODO use transaction

        # get previous max id and add 1
        data = query_db("select max(item_id) as id from data where list = ?", [list_id], one=True)
        if data['id'] is None:
            item_id = 1
        else:
            item_id = data['id'] + 1

        # create item and add all POSTed arguments
        item_data = request.form.to_dict(flat=True)
        perform_db("insert into data (list, item_id, data) values (?, ?, ?)", [list_id, item_id, json.dumps(item_data)])
        item = { 'id': item_id, **request.form.to_dict(flat=True) }
        return item, 201


# setup the API resource routing
api.add_resource(Item, '/<list_id>/<item_id>')
api.add_resource(List, '/<list_id>')


if __name__ == '__main__':
    app.run(debug=True)
