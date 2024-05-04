import pytest
from app import app

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'This app is used to get gists of any Github User, to get info about any user use /gists/username path in url'

def test_get_user_gists_success(client, monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse([{"id": "123", "description": "Test gist"}], 200)

    monkeypatch.setattr("requests.get", mock_get)

    response = client.get('/gists/octocat')
    assert response.status_code == 200
    assert response.json == [{"id": "123", "description": "Test gist"}]

def test_get_user_gists_failure(client, monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse([], 404)

    monkeypatch.setattr("requests.get", mock_get)

    response = client.get('/gists/invaliduser')
    assert response.status_code == 404
    assert response.json == {"error": "please pass a existing user"}

def test_invalid_path(client, monkeypatch):
    response = client.get('/auth/')
    assert response.status_code == 404
    assert response.json == None

