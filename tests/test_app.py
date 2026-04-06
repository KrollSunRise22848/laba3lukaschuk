import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_success(client):
    response = client.post('/register', data={
        'email': 'tests@example.com',
        'password': 'secure123'
    })
    assert response.status_code == 302  # редирект после регистрации

def test_login_success(client):
    # Сначала регистрируем
    client.post('/register', data={
        'email': 'tests@example.com',
        'password': 'secure123'
    })
    # Потом логинимся
    response = client.post('/login', data={
        'email': 'tests@example.com',
        'password': 'secure123'
    })
    assert response.status_code == 302

def test_protected_requires_login(client):
    response = client.get('/protected')
    assert response.status_code == 401  # или 302 на страницу логина