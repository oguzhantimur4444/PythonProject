from abc import ABC,abstractmethod

class Base(ABC):
    def __init__(self,id):
        self.id=id
    @abstractmethod
    def to_dict(self):pass

class User:
    def __init__(self, username, password):
        self.username=username
        self.password=password

class Request(Base):
    maxID=0
    def __init__(self, name, type, mail, personelId, definition, id:int = None):
        if id==None:
            id=Request.maxID
            Request.maxID+=1
        elif id>Request.maxID:
            Request.maxID=id+1
        elif Request.maxID==id:
            id+=1
        
        super().__init__(id)
        self.name=name
        self.type=type
        self.mail=mail
        self.personelId=personelId
        self.definition=definition
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "mail": self.mail,
            "personelId": self.personelId,
            "definition": self.definition,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            mail=data["mail"],
            personelId=data["personelId"],
            definition=data["definition"]
        )

class Personel(User,Base):
    def __init__(self, id, username, password, brim, yetki):
        Base.__init__(self,id)
        User.__init__(self,username,password)
        self.brim=brim
        self.yetki=yetki
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "brim": self.brim,
            "yetki": self.yetki,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            username=data["username"],
            password=data["password"],
            brim=data["brim"],
            yetki=data["yetki"]
        )

