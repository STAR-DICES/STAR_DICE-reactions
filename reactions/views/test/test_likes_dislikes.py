import requests
import json

from reactions.database import db, Like, Dislike
from flask_testing import TestCase # pragma: no cover
from reactions.app import start


class TestLike(TestCase):
    def create_app(self):
        self.app = start(test=True)
        self.context = self.app.app_context()
        self.client = self.app.test_client()
        return self.app

    def tearDown(self):
        with self.context:
            db.drop_all()
    
    def test_single_like_remove_like(self):
        data = {'story_id' : 1, 'user_id' : 1}
        reply = self.client.post('/like', json=data)
        self.assertEqual(reply.status_code, 200)
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
        reply = self.client.delete('/like', json=data)
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNone(l)

    def test_existing_reacted_stories(self):
        reply = self.client.get('/get-reacted-stories/2')
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(json.loads(reply.data), {'stories_id': [1]})

    def test_nonexisting_reacted_stories(self):
        reply = self.client.get('/get-reacted-stories/100')
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(json.loads(reply.data), {'stories_id': []})

    def test_not_existing_story(self):
        data = {'story_id' : 5, 'user_id' : 1}
        reply = self.client.post('/like', json=data)
        self.assertEqual(reply.status_code, 404)

    def test_single_dislike_remove_dislike(self):
        data = {'story_id' : 1, 'user_id' : 1}
        reply = self.client.post('/dislike', json=data)
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
        reply = self.client.delete('/dislike', json=data)
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNone(l)

    def test_like_dislike(self):
        data = {'story_id' : 1, 'user_id' : 1}
        reply = self.client.post('/like', json=data)
        with self.context:
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNone(l)
        reply = self.client.post('/dislike', json=data)
        with self.context:
            l = Dislike.query.filter_by(disliker_id=1, story_id=1).first()
            self.assertIsNotNone(l)
            l = Like.query.filter_by(liker_id=1, story_id=1).first()
            self.assertIsNone(l)

