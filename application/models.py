from application import db
import datetime

class scrapeData(db.Model):
    __tablename__ = "scraped_data_all"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(200), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)