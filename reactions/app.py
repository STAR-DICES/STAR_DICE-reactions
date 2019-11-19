import datetime
import json
import os

from monolith.database import db, Like, Dislike
from reactions.views import blueprints

from flakon import create_app

def start(test = False):
    app = create_app(blueprints=blueprints)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
    if test:
        app.config['TESTING'] = True
        app.config['CELERY_ALWAYS_EAGER'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
    db.init_app(app)
    db.create_all(app=app)
    
    with app.app_context():
        # TODO Initialize env to test
    
    return app

if __name__ == '__main__':
    app = start()
    app.run()
