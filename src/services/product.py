import logging
import traceback

from storage.product import ProductStorage
from models.product import ProductModel

class ProductService:
    def __init__(self):
        self.storage = ProductStorage()

    def insert(self, prod:ProductModel) -> int:
        try:
            id = self.storage.insert(prod)
            prod.setId(id)
            logging.debug(f"[PRODUCT-SERVICE] Product created: {prod.toJson()}")
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")

        return id
            
    def get(self) -> list:
        try:
            ret = self.storage.get()
            if ret is not None:
                logging.debug(f"[PRODUCT-SERVICE] Get all products: {len(ret)} products")
                return ret
        
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")
        
        return None

    def getById(self, id:int) -> ProductModel:
        try:
            ret = self.storage.getById(id)
            if ret is None:
                logging.debug(f"[PRODUCT-SERVICE] Product not found ID:{id}")
                return None
    
            logging.debug(f"[PRODUCT-SERVICE] Get Product: {ret.toJson()}")

            return ret
        except Exception as error:
            logging.error(f"[PRODUCT-SERVICE] Fail: {error} -> {traceback.format_exc()}")

        return None