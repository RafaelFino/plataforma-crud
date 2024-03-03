import logging
from flask import Flask, request
from http import HTTPStatus
from datetime import datetime

from models import ProductModel
from services import ProductService

app = Flask(__name__)
service = ProductService()

def makeResponse(msg: str, args: dict):
    ret = {
        "message": msg,
        "timestamp": datetime.now()
    }

    for key in args:
        ret[key] = args[key]

    return ret

@app.route("/products", methods = ['POST'])
def insert():
    p = None
    try:
        name = request.form['name']
        desc = request.form['desc']
        price = float(request.form['price'])
        p = ProductModel(name, desc, price)
    except Exception as error: 
        errorMsg = f"Error to try process request: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.BAD_REQUEST
    
    try:
        id = service.insert(p)
        logging.info(f"[PRODUCT-API] Product inserted with ID {id}")

    except Exception as error: 
        errorMsg = f"Error to try process request: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR
    
    return makeResponse(f"product created", { "id": id }), HTTPStatus.CREATED

@app.route("/products", methods = ['GET'])
def get():
    try:
        ret = service.get()
        if len(ret) == 0:
            return makeResponse("List all products", { 'count': len(ret) }), HTTPStatus.NOT_FOUND
        
        data = []
        for p in ret:
            data.append(p.toJson())

        return makeResponse("List all products", { "data": data, 'count': len(ret) }), HTTPStatus.OK
    except Exception as error: 
        errorMsg = f"Error to try get all products: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR        

@app.route("/products/<id>", methods = ['GET'])
def get(id):
    try:
        ret = service.getById(id)
        if ret is None:
            return makeResponse(f"Load product from id {id}", { 'id': id }), HTTPStatus.NOT_FOUND

        return makeResponse(f"Load product from id {id}", { "data": ret.toJson() }), HTTPStatus.OK
    except Exception as error: 
        errorMsg = f"Error to try get product id {id}: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR       
