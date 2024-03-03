import json 

class ProductModel:
    def __init__(self, name: str, desc: str, price: float):
        self.Name = name
        self.Desc = desc
        self.Price = price
        self.Id = None

    def setId(self, id: int):
        self.Id = id

    def toDict(self):
        data = { 
            "name": self.Name, 
            "desc": self.Desc, 
            "price": self.Price 
        }

        if self.Id is not None:
            data["id"] = self.Id

        return data

    def toJson(self) -> str:
        return json.dumps(self.toDict())