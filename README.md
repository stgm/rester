# Rester

A generic REST data server based on flask_restful. It can serve data from hardcoded default lists, or you can use a POST request to save arbitrary data in an arbitrary (1-level) namespace.

## Disclaimer

Watch out!

- This server does not persist data between runs, so do not use it in production! If killed, the data will be reset to whatever data is hardcoded in the `rester.py` file.

- This server doesn't have any security measures in place, so do not use it in production! In particular, it should be easy to do denial of service attacks by dumping large data through several POST requests. This data will be saved into local working memory.

- This server isn't safe for handling multiple requests at the same time, so do not use it in production!

## Usage

    python rester.py

## Installation

    pip install flask_restful

## Example data

The server comes with sample data that is available for querying upon start. Currently, there's an unnumbered list of categories (`/categories` endpoint) and a list of menu items (`/menu` endpoint). 

## API

### GET /list

Returns, in JSON, the full data for one list. In case of default data, this might even be an object, as is the case with the example data for `/menu`.

    curl http://127.0.0.1:5000/list

### POST /list

Adds a new item to a list. The full item will be returned, with the new item ID filled in. Hence, the item ID should not be specified in the request. Other attributes can be specified using HTTP POST data.

    curl http://localhost:5000/list -d "description=great stuff" -X POST

### GET /list/1

Returns, in JSON, the data for one item in a list.

    curl http://127.0.0.1:5000/list/1

### DELETE /list/1

Deletes the data for one item in the list. Other item IDs will not be changed.

    curl http://localhost:5000/list/1 -X DELETE

### PUT /list/1

Amends the data for one item in the list. Newly attached data will be merged in and so will not delete existing data.


## Hardcoding data

The `DATA` variable contains all data that's in the server by default. In line with JSON standards, this can be filled with lists (arrays) or dictionaries (objects). Refer to the example data atop the `rester.py` code to learn more.
