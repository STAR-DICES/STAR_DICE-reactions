import requests
import json


stories_url = '127.0.0.1:6000'  # TODO: insert real stories microservice url

class Request:
    def __init__(self, get_story, delete_reaction, add_reaction, timeout=1):
        self._get_story = get_story
        self._delete_reaction = delete_reaction
        self._add_reaction = add_reaction
        self._timeout = timeout

    def get_story(self, story_id):
        return self._get_story(story_id, self._timeout)
    def delete_reaction(self, reaction, story_id):
        return self._delete_reaction(reaction, story_id, self._timeout)
    def add_reaction(self, reaction, story_id):
        return self._add_reaction(reaction, story_id, self._timeout)


class TestResponse:
    def __init__(self, status_code, response_data):
        self.status_code = status_code
        self._json = json.dumps(response_data)

    def json(self):
        return self._json


existing_response = {
    'story': {
        'story_id': 1,
        'title': 'Spooky',
        'text': 'The green zombie waves at the green ghost.',
        'rolls_outcome': ['zombie', 'ghost', 'green', 'goo'],
        'theme': "Halloween",
        'date': '10/10/1010',
        'likes': 10,
        'dislikes': 1,
        'published': True,
        'author_id': 1,
        'author_name': 'Admin'
        }
}

def test_get_story(story_id, timeout):
    if story_id == 1:
        return TestResponse(200, existing_response)
    return TestResponse(404, None)
    
def test_delete_reaction(reaction, story_id, timeout):
    if story_id == 1:
        return TestResponse(200, "")
    return TestResponse(404, None)   
    
def test_add_reaction(reaction, story_id, timeout):
    if story_id == 1:
        return TestResponse(200, "")
    return TestResponse(404, None)
    
def real_delete_reaction(reaction, story_id, timeout):
    return requests.delete(stories_url + "/" + str(reaction) + "/" + str(story_id), timeout=timeout)
    
def real_add_reaction(reaction, story_id, timeout):
    return requests.post(stories_url + "/" + str(reaction) + "/" + str(story_id), timeout=timeout)

def real_get_story(story_id, timeout):
    return requests.get(stories_url + "/story/" + str(story_id), timeout=timeout)


test_request = Request(test_get_story, test_delete_reaction, test_add_reaction)
real_request = Request(real_get_story, real_delete_reaction, real_add_reaction)
