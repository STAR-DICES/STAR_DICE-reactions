import json
import requests
from reactions.database import db, Like, Dislike
from reactions.views.test.TestHelper import TestHelper

class TestLike(TestHelper):
    
    def test_single_like_remove_like(self):
        data = {'story_id' : 1, 'user_id' : 1}
        headers = {'Content-type': 'application/json'}
        reply = self.client.post('/like', json=data, headers=headers)
        self.assertEqual(reply.status_code, 200)
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
        reply = self.client.delete('/like', json=data)
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNone(l)
   
    def test_not_existing_story(self):
        data = {'story_id' : 5, 'user_id' : 1}
        headers = {'Content-type': 'application/json'}
        reply = self.client.post('/like', json=data, headers=headers)
        self.assertEqual(reply.status_code, 404)
        
    def test_single_dislike_remove_dislike(self):
        data = {'story_id' : 1, 'user_id' : 1}
        headers = {'Content-type': 'application/json'}
        reply = self.client.post('/dislike', json=data, headers=headers)
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
        reply = self.client.delete('/dislike', json=data, headers=headers)
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNone(l)
         
    def test_like_dislike(self):
        data = {'story_id' : 1, 'user_id' : 1}
        headers = {'Content-type': 'application/json'}
        reply = self.client.post('/like', json=data, headers=headers)
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNone(l)
        reply = self.client.post('/dislike', json=data, headers=headers)
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNone(l)

