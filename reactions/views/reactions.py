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
    current_user_id = json_data['user_id']
    
    #Retrieve story via stories microservice
    r = requests.get(story_url + "/story/" + story_id)
    if r.status_code == 404:
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
            #Send to stories microservice
            requests.delete(story_url + "/dislike/" + story_id)
        requests.post(story_url + "/like/" + story_id)
        db.session.add(new_like)
        db.session.commit()
        return '', 200
    else:
        return abort(409)

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
    current_user_id = json_data['user_id']

    #Retrieve story via stories microservice
    r = requests.get(story_url + "/story/" + story_id)
    if r.status_code == 404:
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
            #Send to stories microservice 
            requests.delete(story_url + "/like/" + story_id)
        requests.post(story_url + "/dislike/" + story_id)
        db.session.add(new_dislike)
        db.session.commit()
        return '', 200
    else:
        return abort(409)

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
    current_user_id = json_data['user_id']

    #Retrieve story via stories microservice
    r = requests.get(story_url + "/story/" + story_id)
    if r.status_code == 404:
        abort(404)
        
    l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
    if l is None:
        return abort(409)
    else:
        #Send to stories microservice
        requests.delete(story_url + "/like/" + story_id) 
        db.session.delete(l)
        db.session.commit()
        return '', 200
    
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
    current_user_id = json_data['user_id']

    #Retrieve story via stories microservice
    r = requests.get(story_url + "/story/" + story_id)
    if r.status_code == 404:
        abort(404)
    
    d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
    if d is None:
        return abort(409)
    else:
        #Send to stories microservice 
        requests.delete(story_url + "/dislike/" + story_id) 
        db.session.delete(d)
        db.session.commit()
        return '', 200

"""
The route is used to retrieve the stories a user has already reacted to
"""   
@reactions.operation('getReactedStories')
def _get_Reacted_Stories(user_id):
    stories = []
    likes = Like.query.filter_by(user_id=user_id).all()
    for l in likes:
        stories.append(l.story_id)
    dislikes = Dislike.query.filter_by(user_id=user_id).all()
    for d in dislikes:
        stories.append(d.story_id)
    
    return jsonify({'stories_id' : stories})



