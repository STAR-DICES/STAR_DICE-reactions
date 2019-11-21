from flakon import SwaggerBlueprint
from flask import request, jsonify, abort
from reactions.database import db, Like, Dislike
from sqlalchemy.sql.expression import func
import requests
from jsonschema import validate, ValidationError

reactions = SwaggerBlueprint('reactions', __name__, swagger_spec='./reactions/static/react-specs.yaml')

story_url= 'story docker ip goes here'


"""
The route can be used by a logged in user to like a published story.
"""
@reactions.operation('like')
def _like():
    if general_validator('like', request):
        json_data = request.get_json()
        story_id = json_data['story_id']
        current_user_id = json_data['user_id']
        
        #Retrieve story via stories microservice
        r = requests.get(story_url + "/story/" + story_id)
        if r.status_code == 404:
            abort(404)
        
        q = Like.query.filter_by(liker_id=current_user_id, story_id=story_id)
        if q.first() is None:
            new_like = Like()
            new_like.liker_id = current_user_id
            new_like.story_id = story_id
            # remove dislike, if present
            d = Dislike.query.filter_by(disliker_id=current_user_id, story_id=story_id).first()
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
    else:
        abort(400)

"""
The route can be used by a logged in user to dislike a published story.
"""
@reactions.operation('dislike')
def _dislike():
    
    if general_validator('dislike', request):
        json_data = request.get_json()
        story_id = json_data['story_id']
        current_user_id = json_data['user_id']

        #Retrieve story via stories microservice
        r = requests.get(story_url + "/story/" + story_id)
        if r.status_code == 404:
            abort(404)

        q = Dislike.query.filter_by(disliker_id=current_user_id, story_id=story_id)
        if q.first() is None:
            new_dislike = Dislike()
            new_dislike.disliker_id = current_user_id
            new_dislike.story_id = story_id
            # remove like, if present
            l = Like.query.filter_by(liker_id=current_user_id, story_id=story_id).first()
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
    else:
        abort(400)

"""
The route can be used by a logged in user to remove a like
from a published story.
"""
@reactions.operation('remove_like')
def _remove_like():

    if general_validator('remove_like', request):
        json_data = request.get_json()    
        story_id = json_data['story_id']
        current_user_id = json_data['user_id']

        #Retrieve story via stories microservice
        r = requests.get(story_url + "/story/" + story_id)
        if r.status_code == 404:
            abort(404)
            
        l = Like.query.filter_by(liker_id=current_user_id, story_id=story_id).first()
        if l is None:
            return abort(409)
        else:
            #Send to stories microservice
            requests.delete(story_url + "/like/" + story_id) 
            db.session.delete(l)
            db.session.commit()
            return '', 200
    else:
        abort(400)
    
"""
The route can be used by a logged in user and to remove a dislike
from a published story.
"""
@reactions.operation('remove_dislike')
def _remove_dislike():

    if general_validator('remove_like', request):
        json_data = request.get_json()
        story_id = json_data['story_id']
        current_user_id = json_data['user_id']

        #Retrieve story via stories microservice
        r = requests.get(story_url + "/story/" + story_id)
        if r.status_code == 404:
            abort(404)
        
        d = Dislike.query.filter_by(disliker_id=current_user_id, story_id=story_id).first()
        if d is None:
            return abort(409)
        else:
            #Send to stories microservice 
            requests.delete(story_url + "/dislike/" + story_id) 
            db.session.delete(d)
            db.session.commit()
            return '', 200
    else:
        abort(400)

"""
The route is used to retrieve the stories a user has already reacted to
"""   
@reactions.operation('getReactedStories')
def _get_reacted_stories(user_id):
    stories = []
    likes = Like.query.filter_by(user_id=user_id).all()
    for l in likes:
        stories.append(l.story_id)
    dislikes = Dislike.query.filter_by(user_id=user_id).all()
    for d in dislikes:
        stories.append(d.story_id)
    
    return jsonify({'stories_id' : stories})

def general_validator(op_id, request):
    schema= reactions.spec['paths']
    for endpoint in schema.keys():
        for method in schema[endpoint].keys():
            if schema[endpoint][method]['operationId']==op_id:
                op_schema= schema[endpoint][method]['parameters'][0]
                if 'schema' in op_schema:
                    definition= op_schema['schema']['$ref'].split("/")[2]
                    schema= reactions.spec['definitions'][definition]
                    try:
                        validate(request.get_json(), schema=schema)
                        return True
                    except ValidationError as error:
                        return False
                else:
                     return True



