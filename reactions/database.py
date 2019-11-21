# encoding: utf8
import datetime as dt
import enum
import json
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Like(db.Model):
    __tablename__ = 'like'
    
    liker_id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, primary_key=True)
    marked = db.Column(db.Boolean, default = False) # True iff it has been counted in Story.likes
    
class Dislike(db.Model):
    __tablename__ = 'dislike'
    
    disliker_id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, primary_key=True)
    marked = db.Column(db.Boolean, default = False) # True iff it has been counted in Story.likes 