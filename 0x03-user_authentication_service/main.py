#!/usr/bin/env python3
"""
Main file
"""
import requests
BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """ queries and tests user registration """
    payload = {'email': email, 'password': password}
    r = requests.post(BASE_URL+'/users', data=payload)
    assert r.status_code == 200
    d = r.json()
    assert d['email'] == email
    assert d['message'] == 'user created'


def log_in_wrong_password(email: str, password: str) -> None:
    """ test api login endpoint with wrong password """
    payload = {'email': email, 'password': password}
    r = requests.post(BASE_URL+'/sessions', data=payload)
    assert r.status_code == 401


def profile_unlogged():
    """ tries to get a profile with wrong session id """
    cookies = dict(session_id='wrongone')
    r = requests.get(BASE_URL+'/profile', cookies=cookies)
    assert r.status_code == 403


def log_in(email: str, password: str) -> str:
    """ tests login endpoint and returns session id """
    payload = {'email': email, 'password': password}
    r = requests.post(BASE_URL+'/sessions', data=payload)
    assert r.status_code == 200
    d = r.json()
    assert d['email'] == email
    assert d['message'] == 'logged in'
    assert r.cookies['session_id'] is not None
    return r.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """ tries to get a profile """
    r = requests.get(BASE_URL+'/profile', cookies={'session_id': session_id})
    assert r.status_code == 200
    assert r.json()['email'] is not None


def log_out(session_id: str) -> None:
    """ Test logout endpoint """
    r = requests.delete(BASE_URL+'/sessions',
                        cookies={'session_id': session_id})
    assert r.status_code == 200
    assert len(r.history) > 0


def reset_password_token(email: str) -> str:
    """ Test password reset endpoint for getting reset token """
    r = requests.post(BASE_URL+'/reset_password', data={'email': email})
    assert r.status_code == 200
    d = r.json()
    assert d['reset_token'] is not None
    return d['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Tests password update endpoint """
    data = {
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
        }
    r = requests.put(BASE_URL+'/reset_password', data=data)
    assert r.status_code == 200
    d = r.json()
    assert d['message'] == 'Password updated'


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
