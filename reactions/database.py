# encoding: utf8
import datetime as dt
import enum
import json

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from monolith.classes import Die, DiceSet


db = SQLAlchemy()

class Like(db.Model):
    __tablename__ = 'like'
    
    liker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    liker = relationship('User', foreign_keys='Like.liker_id')

    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), primary_key=True)
    author = relationship('Story', foreign_keys='Like.story_id')

    marked = db.Column(db.Boolean, default = False) # True iff it has been counted in Story.likes
    
class Dislike(db.Model):
    __tablename__ = 'dislike'
    
    disliker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    disliker = relationship('User', foreign_keys='Dislike.disliker_id')

    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), primary_key=True)
    author = relationship('Story', foreign_keys='Dislike.story_id')

    marked = db.Column(db.Boolean, default = False) # True iff it has been counted in Story.likes 
