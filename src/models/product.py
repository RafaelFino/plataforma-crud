from datetime import datetime
import json 

class ProductModel:
    def __init__(self, name: str, desc: str, price: float):
        self.Name = name
        self.Desc = desc
        self.Price = price
        self.UpdatedAt = datetime.now()
        self.InsertedAt = datetime.now()

    def setId(self, id: int):
        self.Id = id

    def setInsertedAt(self, when: datetime):
        self.InsertedAt = when

    def setUpdatedAt(self, when: datetime):
        self.UpdatedAt = when

    def toJson(self) -> str:
        return json.dumps(self, indent=4)