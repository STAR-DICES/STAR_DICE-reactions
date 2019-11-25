import datetime
import json
import os
from reactions.database import db, Like, Dislike
from reactions.views import blueprints
from flakon import create_app
from swagger_ui import api_doc

def start(test = False):
    app = create_app(blueprints=blueprints)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reactions.db'
    if test:
        app.config['TESTING'] = True
        app.config['CELERY_ALWAYS_EAGER'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    api_doc(app, config_path='./reactions/react-specs.yaml', url_prefix='/api', title='API doc')
    db.init_app(app)
    db.create_all(app=app)
    
    with app.app_context():
        q = db.session.query(Like)
        like = q.first()
        if like is None:
            example = Like()
            example.story_id= 1
            example.liker_id= 2
            db.session.add(example)
            db.session.commit()
        s = db.session.query(Dislike)
        dislike = q.first()
        if dislike is None:
            example = Dislike()
            example.story_id=1
            example.disliker_id= 3
            db.session.add(example)
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = start()
    app.run(host=0.0.0.0)
