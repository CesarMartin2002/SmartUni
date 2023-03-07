import json

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_taquilla_list(client):
    response = client.get("/taquilla")
    assert response.status_code == 200
    assert len(response.json()) == 16

def test_taquilla_create(client):
    data = {
        "ala": "norte",
        "planta": 1,
        "pasillo": 1
    }
    response = client.post("/taquilla", json.dumps(data))
    assert response.status_code == 201
    assert response.json()["id"] == 17
    assert response.json()["ala"] == "norte"
    assert response.json()["planta"] == 1
    assert response.json()["pasillo"] == 1

def test_taquilla_delete(client):
    response = client.delete("/taquilla/17")
    assert response.status_code == 204
