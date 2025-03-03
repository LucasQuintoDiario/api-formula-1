import requests


def test_home():
    url = 'http://localhost:8000/'  
    response = requests.get(url)
    assert response.status_code == 200

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


def test_delete_history():
    get_id_url = 'http://localhost:8000/getid/'
    response = requests.get(get_id_url)
    assert response.status_code == 200
    session_id = response.json()
    delete_url = 'http://localhost:8000/delete_history/'
    delete_payload = {"id": session_id}
    delete_response = requests.delete(delete_url, json=delete_payload)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Historial eliminado correctamente"