import pytest
from flask_jwt_extended import create_access_token
from server import app, db, DriverPosting, User
from datetime import datetime, timedelta


def generate_token(user_id):
    with app.app_context():
        return create_access_token(identity=user_id)

def generate_token_by_tel_via_login(client, tel='19999999999'):
    res = client.post('/login', json={'Tel': tel, 'password': 'abc123'})
    assert res.status_code == 200
    return res.get_json()['token']

def register_user(client, tel='19999999999', is_driver=True):
    res = client.post('/register', json={
        'name': 'TestUser',
        'tel': tel.lower(),
        'password': 'abc123',
        'confirmPassword': 'abc123',
        'isDriver': is_driver
    })
    # Ensure user is committed to DB for immediate queries
    with app.app_context():
        db.session.commit()
    return res

def test_register_success(client):
    res = register_user(client)
    assert res.status_code == 201

def test_register_duplicate(client):
    register_user(client)
    res = register_user(client)
    assert res.status_code == 400

def test_login_success(client):
    register_user(client)
    res = client.post('/login', json={'Tel': '19999999999', 'password': 'abc123'})
    assert res.status_code == 200
    assert 'token' in res.get_json()

def test_login_wrong_password(client):
    register_user(client)
    res = client.post('/login', json={'Tel': '19999999999', 'password': 'wrong'})
    assert res.status_code == 401

def test_userinfo(client):
    register_user(client)
    token = generate_token_by_tel_via_login(client, '19999999999')
    res = client.get('/userinfo', headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 200

def test_register_driver(client):
    register_user(client, is_driver=False)
    token = generate_token_by_tel_via_login(client, '19999999999')
    res = client.post('/register_driver', headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 200

def test_unregister_driver(client):
    register_user(client, is_driver=True)
    token = generate_token_by_tel_via_login(client, '19999999999')
    res = client.post('/unregister_driver', headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 200

def test_post_driver_posting_success(client):
    # 先注册非司机用户
    register_user(client, is_driver=False)
    token = generate_token_by_tel_via_login(client, '19999999999')

    # 申请成为司机
    res = client.post('/register_driver', headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 200

    # 司机身份确认后发布行程
    res = client.post('/post_driver_posting', json={
        "From": "A", "To": "B",
        "FromLat": 30.0, "FromLng": 120.0,
        "ToLat": 30.1, "ToLng": 120.1,
        "DepartureTime": (datetime.now() + timedelta(days=1)).isoformat(),
        "SeatsAvailable": 3,
        "Fare": 50.0,
        "PlateNumber": "沪A12345"
    }, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 201

def test_post_driver_posting_missing_fields(client):
    register_user(client, is_driver=True)
    token = generate_token_by_tel_via_login(client, '19999999999')
    res = client.post('/post_driver_posting', json={
        "From": "A"  # 缺失大量字段
    }, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 400

def test_get_driver_postings(client):
    test_post_driver_posting_success(client)
    token = generate_token_by_tel_via_login(client, '19999999999')
    res = client.get('/get_driver_postings', headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_join_trip(client):
    test_post_driver_posting_success(client)
    register_user(client, tel='19999999998', is_driver=False)
    token = generate_token_by_tel_via_login(client, '19999999998')
    res = client.post('/join_trip', json={"PostingID": 1}, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 201

def test_join_trip_twice(client):
    test_join_trip(client)
    token = generate_token_by_tel_via_login(client, '19999999998')
    res = client.post('/join_trip', json={"PostingID": 1}, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 400

def test_my_trip(client):
    test_join_trip(client)
    token = generate_token_by_tel_via_login(client, '19999999998')
    res = client.get('/my_trip', headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_cancel_trip(client):
    test_join_trip(client)
    token = generate_token_by_tel_via_login(client, '19999999998')
    res = client.post('/cancel_trip', json={"PostingID": 1}, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    assert res.status_code == 200