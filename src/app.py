#!/bin/env python3

import logging
from flask import Flask, request, jsonify
from http import HTTPStatus
from datetime import datetime
import json 

from models.product import ProductModel
from services.product import ProductService

print("Starting...")

app = Flask(__name__)
service = ProductService()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def makeResponse(msg: str, args: dict = {}):
    ret = {
        "message": msg,
        "timestamp": datetime.now().isoformat()
    }

    for key in args:
        ret[key] = args[key]

    return ret

@app.route("/products", methods = ['POST'])
def insert():
    p = None
    try:
        data = request.json
        name = data['name']
        desc = data['desc']
        price = float(data['price'])
        p = ProductModel(name, desc, price)
    except Exception as error: 
        errorMsg = f"Error to try process request: Invalid request {error} -> {data}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.BAD_REQUEST
    
    try:
        id = service.insert(p)

        if id is None: 
            errorMsg = f"Fail to insert Product {p}"
            logging.error(f"[PRODUCT-API] {errorMsg} ")
            return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR
        
        p.setId(id)

    except Exception as error: 
        errorMsg = f"Error to try process request: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg} ")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR
    
    logging.info(f"[PRODUCT-API] Product inserted with ID {id}")
    return makeResponse(f"product created", { "id": id }), HTTPStatus.CREATED

@app.route("/products", methods = ['GET'])
def get():
    try:
        ret = service.get()
        if len(ret) == 0:
            return makeResponse("All products", { 'count': len(ret) }), HTTPStatus.NO_CONTENT
        
        data = []
        for p in ret:
            logging.debug(f"[PRODUCT-API] Add item to response: {p.toJson()}")
            data.append(p.toDict())

        return makeResponse("All products", { "data": data, 'count': len(ret) }), HTTPStatus.OK
    except Exception as error: 
        errorMsg = f"Error to try get all products: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR        

@app.route("/products/<id>", methods = ['GET'])
def getById(id):
    try:
        ret = service.getById(id)
        if ret is None:
            logging.debug(f"[PRODUCT-API] Product not found ID:{id}")
            return makeResponse(f"Product not found", { "id": id }), HTTPStatus.NO_CONTENT

        return makeResponse(f"Product id {id}", { "data": ret.toDict() }), HTTPStatus.OK
    except Exception as error: 
        errorMsg = f"Error to try get product id {id}: {error}"
        logging.error(f"[PRODUCT-API] {errorMsg}")
        return makeResponse(errorMsg), HTTPStatus.INTERNAL_SERVER_ERROR       

print("Exiting...")