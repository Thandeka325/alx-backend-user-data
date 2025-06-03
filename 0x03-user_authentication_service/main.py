#!/usr/bin/env python3
"""
Main module for testing authentication service
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    response = requests.post(
        f"{BASE_URL}/users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "user created"
    }

    # Trying to register same user again should fail
    response = requests.post(
        f"{BASE_URL}/users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password"""
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login with correct credentials"""
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "logged in"
    }
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """Test accessing profile while logged out"""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test accessing profile with a valid session"""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Test logout with valid session"""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """Test requesting a password reset token"""
    response = requests.post(
        f"{BASE_URL}/reset_password",
        data={"email": email}
    )
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp.get("email") == email
    assert "reset_token" in json_resp
    return json_resp["reset_token"]


def update_password(
    email: str, reset_token: str, new_password: str
) -> None:
    """Test updating the password"""
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "message": "Password updated"
    }


# Predefined test credentials
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
