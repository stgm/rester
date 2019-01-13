# Rester

A generic REST data server based on flask_restful. It can serve data from hardcoded default lists, or you can use a POST request to save arbitrary data in an arbitrary (1-level) namespace.

## Disclaimer

Watch out!

- This server doesn't have any security measures in place, so do not use it in production! In particular, it should be easy to do denial of service attacks by dumping large data through several POST requests. This data will be saved into local working memory.

- This server isn't safe for handling multiple requests at the same time, so do not use it in production!

## Usage

    FLASK_APP=rester.py flask run

## Installation

    pip install flask_restful
    git clone https://github.com/stgm/rester.git
    cd rester

If running in the [CS50 IDE](https://cs50.io), make sure that you have enabled public sharing of your web app. In the IDE, go to Share -> Application and check the Public checkbox.

## Example data

The server comes with sample data that is available for querying upon start. Currently, there's an unnumbered list of categories (`/categories` endpoint) and a list of menu items (`/menu` endpoint). 

## API

### GET /list

Returns, in JSON, the full data for one list. In case of default data, this might even be an object, as is the case with the example data for `/menu`.

    curl http://localhost:8080/list

### POST /list

Adds a new item to a list. The full item will be returned, with the new item ID filled in. Hence, the item ID should not be specified in the request. Other attributes can be specified using HTTP POST data.

    curl http://localhost:8080/list -d "description=great stuff" -X POST

### GET /list/1

Returns, in JSON, the data for one item in a list.

    curl http://localhost:8080/list/1

### DELETE /list/1

Deletes the data for one item in the list. Other item IDs will not be changed.

    curl http://localhost:8080/list/1 -X DELETE

### PUT /list/1

Amends the data for one item in the list. Newly attached data will be merged in and so will not delete existing data.

