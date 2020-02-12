from application import db
import datetime
from flask_login import UserMixin

class scrapeData(db.Model):
    __tablename__ = "scraped_data_all"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    link = db.Column(db.String(500), nullable = False)
    source = db.Column(db.String(200), nullable = False)
    keyword = db.Column(db.Integer, db.ForeignKey('keyword.id'))
    date = db.Column(db.DateTime(), default = datetime.datetime.utcnow)

class Keyword(db.Model):
    __tablename__ = "keyword"
    id = db.Column(db.Integer, primary_key = True)
    keyword = db.Column(db.String(100))

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    BBC_quant = db.Column(db.Integer)
    TS_quant = db.Column(db.Integer)
    DM_quant = db.Column(db.Integer)

class User_Search(db.Model):
    __tablename__ = "user_search"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    keyword_id = db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'))
