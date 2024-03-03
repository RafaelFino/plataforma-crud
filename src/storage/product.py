import sqlite3
from models import ProductModel

class ProductStorage:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.create()

    def create(self):
        create = f"CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            name TEXT NOT NULL,
            desc TEXT DEFAULT NULL,
            price REAL DEFAULT 0,
            inserted_at TIMESTAMP DEFAULT DATETIME('now'),
            updated_at TIMESTAMP DEFAULT DATETIME('now')
        )"
        cur = self.conn.cursor()
        cur.execute(create)

    def insert(self, product: ProductModel) -> int:
        insert = f"INSERT INTO Products (name, desc, price) 
        VALUES 
        (?, ?, ?)"

        cur = self.conn.cursor()
        result = cur.execute(insert, product.Name, product.Desc, product.Price)
        return result.lastrowid
    
    def get(self) -> list:
        query = f"
        SELECT
            id,
            name,
            desc,
            price,
            inserted_at,
            updated_at
        FROM
            Products
        ORDER BY
            id, 
            updated_at
        "

        cur = self.conn.cursor()

        ret = []

        for row in cur.execute(query):
            p = ProductModel(row['name'], row['desc'], row['price'])
            p.setId(row['id'])
            p.setInsertedAt = row['inserted_at']
            p.setUpdatedAt = row['updated_at']

            ret.append(p)

        return ret
    
    def getByID(self, id: int) -> ProductModel:
        query = f"
        SELECT
            id,
            name,
            desc,
            price,
            inserted_at,
            updated_at
        FROM
            Products
        WHERE
            id = ? 
        ORDER BY
            id, 
            updated_at
        "

        cur = self.conn.cursor()
        result = cur.execute(query, id)
        row = result.fetchone()

        if row is None:
            return None

        p = ProductModel(row['name'], row['desc'], row['price'])
        p.setId(row['id'])
        p.setInsertedAt = row['inserted_at']
        p.setUpdatedAt = row['updated_at']

        return p