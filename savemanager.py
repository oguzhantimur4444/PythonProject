import json
from utils import *

class SaveManager:
    def __init__(self):
        self.personeller=[]
        self.requests=[]
        self.Load()
    def Load(self):
        with open("save.json","r") as f:
            d = json.load(f)
        self.personeller=[Personel.from_dict(p) for p in d.get("personeller",[])]
        self.requests=[Request.from_dict(r) for r in d.get("requests",[])]
    def to_dict(self):
        return {
            "personeller": [personel.to_dict() for personel in self.personeller],
            "requests": [request.to_dict() for request in self.requests],
        }
    def Save(self):
        with open("save.json","w") as f:
            f.write(json.dumps(self.to_dict(),indent=4))
    def AddPersonel(self,uName,psw,brm,ytk):
        self.personeller.append(Personel(uName,psw,brm,ytk))
        self.Save()