"""Tests for user management endpoints and progress reset."""


# ── GET /api/users — admin only ───────────────────────────────────────────────

def test_admin_can_list_users(client, admin_headers, user_token):
    response = client.get("/api/users", headers=admin_headers)
    assert response.status_code == 200
    users = response.json()
    usernames = [u["username"] for u in users]
    assert "admin" in usernames
    assert "amy" in usernames


def test_user_cannot_list_users(client, user_headers):
    response = client.get("/api/users", headers=user_headers)
    assert response.status_code == 403


def test_unauthenticated_cannot_list_users(client):
    response = client.get("/api/users")
    assert response.status_code == 401


def test_user_list_includes_role(client, admin_headers):
    response = client.get("/api/users", headers=admin_headers)
    for user in response.json():
        assert "role" in user


# ── GET /api/users/{id} — admin only ─────────────────────────────────────────

def test_admin_can_get_user_detail(client, admin_headers, user_token):
    users = client.get("/api/users", headers=admin_headers).json()
    amy = next(u for u in users if u["username"] == "amy")
    response = client.get(f"/api/users/{amy['id']}", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "amy"
    assert "card_views" in data


def test_user_cannot_get_user_detail(client, user_headers, admin_headers):
    users = client.get("/api/users", headers=admin_headers).json()
    amy = next(u for u in users if u["username"] == "amy")
    response = client.get(f"/api/users/{amy['id']}", headers=user_headers)
    assert response.status_code == 403


def test_get_nonexistent_user_returns_404(client, admin_headers):
    response = client.get("/api/users/9999", headers=admin_headers)
    assert response.status_code == 404


# ── PUT /api/users/{id} — admin only ─────────────────────────────────────────

def test_admin_can_change_username(client, admin_headers, user_token):
    users = client.get("/api/users", headers=admin_headers).json()
    amy = next(u for u in users if u["username"] == "amy")
    response = client.put(f"/api/users/{amy['id']}", json={"username": "amelia"}, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "amelia"


def test_admin_can_change_role_to_admin(client, admin_headers, user_token):
    users = client.get("/api/users", headers=admin_headers).json()
    amy = next(u for u in users if u["username"] == "amy")
    response = client.put(f"/api/users/{amy['id']}", json={"role": "admin"}, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_admin_can_reset_another_users_password(client, admin_headers, user_token):
    users = client.get("/api/users", headers=admin_headers).json()
    amy = next(u for u in users if u["username"] == "amy")
    client.put(f"/api/users/{amy['id']}", json={"password": "newpass"}, headers=admin_headers)
    login = client.post("/api/login", json={"username": "amy", "password": "newpass"})
    assert login.status_code == 200


def test_invalid_role_value_returns_422(client, admin_headers, user_token):
    users = client.get("/api/users", headers=admin_headers).json()
    amy = next(u for u in users if u["username"] == "amy")
    response = client.put(f"/api/users/{amy['id']}", json={"role": "superuser"}, headers=admin_headers)
    assert response.status_code == 422


def test_user_cannot_update_another_user(client, user_headers, admin_headers):
    users = client.get("/api/users", headers=admin_headers).json()
    admin = next(u for u in users if u["username"] == "admin")
    response = client.put(f"/api/users/{admin['id']}", json={"username": "hacked"}, headers=user_headers)
    assert response.status_code == 403


def test_update_nonexistent_user_returns_404(client, admin_headers):
    response = client.put("/api/users/9999", json={"username": "x"}, headers=admin_headers)
    assert response.status_code == 404


# ── DELETE /api/users/{id} — admin only ──────────────────────────────────────

def test_admin_can_delete_user(client, admin_headers, user_token):
    users = client.get("/api/users", headers=admin_headers).json()
    amy = next(u for u in users if u["username"] == "amy")
    response = client.delete(f"/api/users/{amy['id']}", headers=admin_headers)
    assert response.status_code == 200
    # user is gone
    assert client.get(f"/api/users/{amy['id']}", headers=admin_headers).status_code == 404


def test_admin_cannot_delete_themselves(client, admin_headers):
    users = client.get("/api/users", headers=admin_headers).json()
    admin = next(u for u in users if u["username"] == "admin")
    response = client.delete(f"/api/users/{admin['id']}", headers=admin_headers)
    assert response.status_code == 403


def test_user_cannot_delete_another_user(client, user_headers, admin_headers):
    users = client.get("/api/users", headers=admin_headers).json()
    admin = next(u for u in users if u["username"] == "admin")
    response = client.delete(f"/api/users/{admin['id']}", headers=user_headers)
    assert response.status_code == 403


def test_delete_nonexistent_user_returns_404(client, admin_headers):
    response = client.delete("/api/users/9999", headers=admin_headers)
    assert response.status_code == 404


def test_deleting_user_removes_their_card_views(client, admin_headers, user_headers, user_token, sample_card):
    # record a view as amy
    client.post(f"/api/flashcards/{sample_card['id']}/view", headers=user_headers)
    users = client.get("/api/users", headers=admin_headers).json()
    amy = next(u for u in users if u["username"] == "amy")
    # delete amy
    client.delete(f"/api/users/{amy['id']}", headers=admin_headers)
    # amy is gone
    assert client.get(f"/api/users/{amy['id']}", headers=admin_headers).status_code == 404


# ── POST /api/users/{id}/reset-progress ──────────────────────────────────────

def test_user_can_reset_own_progress(client, user_headers, user_token, sample_card):
    client.put(f"/api/flashcards/{sample_card['id']}/studied", json={"studied": True}, headers=user_headers)
    me = client.get("/api/me", headers=user_headers).json()
    user_id = me["id"]
    response = client.post(f"/api/users/{user_id}/reset-progress", headers=user_headers)
    assert response.status_code == 200
    # studied is now False
    cards = client.get("/api/flashcards", headers=user_headers).json()
    card = next(c for c in cards if c["id"] == sample_card["id"])
    assert card["studied"] is False


def test_admin_can_reset_another_users_progress(client, admin_headers, user_headers, sample_card):
    client.put(f"/api/flashcards/{sample_card['id']}/studied", json={"studied": True}, headers=user_headers)
    me = client.get("/api/me", headers=user_headers).json()
    user_id = me["id"]
    response = client.post(f"/api/users/{user_id}/reset-progress", headers=admin_headers)
    assert response.status_code == 200


def test_user_cannot_reset_another_users_progress(client, user_headers, admin_headers):
    users = client.get("/api/users", headers=admin_headers).json()
    admin = next(u for u in users if u["username"] == "admin")
    response = client.post(f"/api/users/{admin['id']}/reset-progress", headers=user_headers)
    assert response.status_code == 403


def test_reset_progress_unauthenticated_returns_401(client):
    response = client.post("/api/users/1/reset-progress")
    assert response.status_code == 401
