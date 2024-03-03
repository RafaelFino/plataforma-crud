import logging

from storage import ProductStorage
from models import ProductModel

class ProductService:
    def __init__(self):
        self.db = ProductStorage("products.db")

    def insert(self, prod:ProductModel) -> int:
        id = self.db.insert(prod)
        prod.setId(id)
        logging.debug(f"[PRODUCT-SERVICE] Product inserted: {prod.toJson()}")

    def get(self) -> list:
        ret = self.db.get()
        logging.debug(f"[PRODUCT-SERVICE] Get all products: {len(ret)} products")

        return ret
    
    def getById(self, id:int) -> ProductModel:
        ret = self.getById(id)
        logging.debug(f"[PRODUCT-SERVICE] Get Product: {ret.toJson()}")

        return ret