from flask.ext.sqlalchemy import SQLAlchemy
from . import db

class Corporation(db.Model):
    __tablename__ = 'corporation'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), unique=True)
    license_number = db.Column(db.String(20), unique=True)
    credit_number = db.Column(db.String(20), unique=True)
    seal = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    legal_representive_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    pictures = db.relationship('Picture', backref='corporation', lazy='dynamic')

    def __init__(self, name, license_number, credit_number, seal, description, legal_representive_id):
        # self.id = id
        self.name = name
        self.license_number = license_number
        self.credit_number = credit_number
        self.seal = seal
        self.description = description

    def __repr__(self):
        return "企业:" + self.name


class Pictures(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80))
    path = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    updated = db.Column(db.Boolean)
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __init__(self, name, path, date, updated, corporation_id, person_id):
        # self.id = id
        self.name = name
        self.path = path
        self.date = date
        self.updated = updated
        self.corporation_id = corporation_id
        self.person_id = person_id

    def __repr__(self):
        return "图像：" + self.name


class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(20))
    id_number = db.Column(db.String(20))
    mate_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    pictures = db.relationship('Picture',backref='')
    def __init__(self):
        pass



