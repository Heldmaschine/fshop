from app import db

class Flower(db.Model):
    __table__ = db.Model.metadata.tables['ftable']
    id = __table__.c.id_flower
    name = __table__.c.name_flower
    price =__table__.c.price
    category =  __table__.c.category
    url = __table__.c.url
    def __repr__(self):
        return '<Flower %r>' % (self.name)

class User(db.Model):
    __table__ = db.Model.metadata.tables['tusers']
    id = __table__.c.uid
    username = __table__.c.username
    name  = __table__.c.name
    email  = __table__.c.email
    password  = __table__.c.password
    def __repr__(self):
        return '<user %r>' % (self.username)
    def __init__(self, username, email, name, password):
        self.username = username
        self.email =email
        self.name = name
        self.password = password

class Category(db.Model):
    __table__ = db.Model.metadata.tables['category']
    id = __table__.c.id
    name  = __table__.c.name
    url  = __table__.c.url
    def __repr__(self):
        return '<Category %r>' % (self.url)


class Bill(db.Model):
    __table__ = db.Model.metadata.tables['bills']
    id = __table__.c.id
    delivery_place = __table__.c.delivery_place
    delivery_date = __table__.c.delivery_date
    bill_date = __table__.c.bill_date
    amount = __table__.c.amount
    debit_card = __table__.c.debit_card
    username = __table__.c.username
    def init(self, id, username, delivery_date, delivery_place, bill_date, amount, debit_card, delivery_id):
        self.id = id
        self.username = username
        self.delivery_date = delivery_date
        self.delivery_place = delivery_place
        self.bill_date = bill_date
        self.amount = amount
        self.debit_card = debit_card
