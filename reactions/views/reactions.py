from flakon import SwaggerBlueprint
from flask import request, jsonify, abort
from monolith.database import db, Story, Like, Dislike
from sqlalchemy.sql.expression import func

from jsonschema import validate, ValidationError

reactions = SwaggerBlueprint('reactions', __name__, swagger_spec='./reactions/views/react-specs.yaml')

schema= react.spec['definitions']
reaction_schema=schema['Reaction']

"""
The route can be used by a logged in user to like a published story.
"""
@reactions.operation('like')
def _like():

    json_data = request.get_json()
    try:
        validate(json_data, schema=reaction_schema)
    except ValidationError as error:
        return abort(400)
    
    story_id = json_data['story_id']
    user_id = json_data['user_id']
    
    story = None #TODO Retrieve story via stories microservice
    if story is None:
        abort(404)

    q = Like.query.filter_by(liker_id=current_user.id, story_id=story_id)
    if q.first() is None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.story_id = story_id
        # remove dislike, if present
        d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
        if d is not None: 
            db.session.delete(d)
            #TODO Send to stories microservice 
            #async_like.delay(story_id, True)
        else:
            #TODO Send to stories microservice 
            #async_like.delay(story_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'message' : 'Like added!'})
    else:
        return jsonify({'message' : 'You\'ve already liked this story!'})

"""
The route can be used by a logged in user to dislike a published story.
"""
@reactions.operation('dislike')
def _dislike():

    json_data = request.get_json()
    try:
        validate(json_data, schema=reaction_schema)
    except ValidationError as error:
        return abort(400)
    
    story_id = json_data['story_id']
    user_id = json_data['user_id']

    story = None #TODO Retrieve story via stories microservice
    if story is None:
        abort(404)

    q = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id)
    if q.first() is None:
        new_dislike = Dislike()
        new_dislike.disliker_id = current_user.id
        new_dislike.story_id = story_id
        # remove like, if present
        l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
        if l is not None:
            db.session.delete(l)
            #TODO Send to stories microservice 
            #async_dislike.delay(story_id, True)
        else:
            #TODO Send to stories microservice 
            #async_dislike.delay(story_id)
        db.session.add(new_dislike)
        db.session.commit()
        return jsonify({'message' : 'Dislike added!'})
    else:
        return jsonify({'message' : 'You\'ve already disliked this story!'})

"""
The route can be used by a logged in user to remove a like
from a published story.
"""
@reactions.operation('remove_like')
def _remove_like():

    json_data = request.get_json()
    try:
        validate(json_data, schema=reaction_schema)
    except ValidationError as error:
        return abort(400)
    
    story_id = json_data['story_id']
    user_id = json_data['user_id']

    story = None #TODO Retrieve story via stories microservice
    if story is None:
        abort(404)
        
    l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
    if l is None:
        return jsonify({'message' : 'You have to like it first!'})
    else:
        #TODO Send to stories microservice 
        #async_remove_like.delay(story_id)
        db.session.delete(l)
        db.session.commit()
        return jsonify({'message' : 'You removed your like'})
    
"""
The route can be used by a logged in user and to remove a dislike
from a published story.
"""
@reactions.operation('remove_dislike')
def _remove_dislike():

    json_data = request.get_json()
    try:
        validate(json_data, schema=reaction_schema)
    except ValidationError as error:
        return abort(400)
    
    story_id = json_data['story_id']
    user_id = json_data['user_id']

    story = None #TODO Retrieve story via stories microservice
    if story is None:
        abort(404)
    
    d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
    if d is None:
        return jsonify({'message' : 'You didn\'t dislike it yet..'})
    else:
        #TODO Send to stories microservice 
        #async_remove_dislike.delay(story_id)
        db.session.delete(d)
        db.session.commit()
        return jsonify({'message' : 'You removed your dislike!'})
