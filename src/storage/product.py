import logging
import sqlite3
from models.product import ProductModel

class ProductStorage:
    def __init__(self):
        self.conn = sqlite3.connect("products-database.sqlite", check_same_thread=False)
        self.__create()

    def __create(self):
        if self.conn is None:
            logging.error(f"[PRODUCT-STORAGE] Connection error!")

        create = f"""
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL,
    desc TEXT DEFAULT NULL,
    price REAL DEFAULT 0
);
        """
        try:
            cur = self.conn.cursor()
            cur.execute(create)
        except Exception as error: 
            logging.error(f"[PRODUCT-STORAGE] Fail to create table: {error}")      
            raise error     

    def insert(self, product: ProductModel) -> int:
        insert = f"""
INSERT INTO Products (name, desc, price) 
VALUES 
(?, ?, ?)
        """

          
        cur = self.conn.cursor()
        result = cur.execute(insert, (product.Name, product.Desc, product.Price) )
        self.conn.commit()

        id = result.lastrowid
        product.setId(id)
        logging.debug(f"[PRODUCT-STORAGE] Product created: {product.toJson()}")
        return id
    
    def get(self) -> list:
        query = f"""
SELECT
    id,
    name,
    desc,
    price
FROM
    Products
ORDER BY
    id
        """

        cur = self.conn.cursor()

        ret = []

        for row in cur.execute(query):
            p = ProductModel(row[1], row[2], float(row[3]))
            p.setId(int(row[0]))

            ret.append(p)

        return ret
    
    def getById(self, id: int) -> ProductModel:
        query = f"""
SELECT
    id,
    name,
    desc,
    price
FROM
    Products
WHERE
    id = ? 
ORDER BY
    id
        """

        cur = self.conn.cursor()
        result = cur.execute(query, (id) )
        row = result.fetchone()

        if row is None:
            return None

        p = ProductModel(row[1], row[2], float(row[3]))
        p.setId(int(row[0]))

        return p