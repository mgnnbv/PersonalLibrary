from main import User

def test_password_hash():
    u = User(username="a", email="a", password_hash="abc")
    assert isinstance(u.password_hash, str)
