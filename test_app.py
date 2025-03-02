import requests


def test_home():
    url = 'http://localhost:8000/'  
    response = requests.get(url)
    assert response.status_code == 200
    assert "Cuál es tu duda de F1?" in response.text

def test_question():
    payload = {"prompt": "¿Quién ganó el campeonato de F1 en 2023?"}
    url = 'http://localhost:8000/question/'  
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert isinstance(response.json(), str)

def test_get_id():
    url = 'http://localhost:8000/getid/'
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), str)

def test_consult():
    url = 'http://localhost:8000/consult/'
    payload = {"id": "401435ca-a5bf-4356-879a-a79044c877ca"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_history_not_found():
    url = 'http://localhost:8000/delete_history/'
    payload = {"id": "non-existing-id"}
    response = requests.delete(url, json=payload)
    assert response.status_code == 500
    assert response.json()["detail"] == "Error al eliminar el historial"