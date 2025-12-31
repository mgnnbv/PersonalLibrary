

def test_register_success(client):
    resp = client.post("/register", data={
        "username": "john",
        "email": "test@mail.com",
        "password": "123"
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert "Регистрация успешно завершена" in resp.data
