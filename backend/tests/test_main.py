from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_is_up():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'Hello': 'world'}


def test_translate_rus_bur():
    response = client.post('/translate/rus_bur', json={'text': 'Работает'})
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        'text': 'Работает',
        'translation': ['Ажаллана']
    }


def test_translate_bur_rus():
    response = client.post('/translate/bur_rus', json={'text': 'Ажаллана'})
    assert response.status_code == 200
    assert response.json() == {
        'text': 'Ажаллана',
        'translation': ['трудящийся']
    }
