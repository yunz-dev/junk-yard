"""Tests for flashcard CRUD endpoints and per-user progress."""


# ── GET /api/flashcards — public ──────────────────────────────────────────────

def test_get_flashcards_unauthenticated(client, sample_card):
    response = client.get("/api/flashcards")
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) >= 1
    # studied defaults to False for unauthenticated users
    assert cards[0]["studied"] is False


def test_get_flashcards_category_filter(client, admin_headers):
    client.post("/api/flashcards", json={"chinese": "一", "pinyin": "yī", "english": "one", "category": "Numbers"}, headers=admin_headers)
    client.post("/api/flashcards", json={"chinese": "你好", "pinyin": "nǐ hǎo", "english": "hello", "category": "Greetings"}, headers=admin_headers)
    response = client.get("/api/flashcards?category=Numbers")
    assert response.status_code == 200
    cards = response.json()
    assert all(c["category"] == "Numbers" for c in cards)


def test_get_flashcard_by_id(client, sample_card):
    response = client.get(f"/api/flashcards/{sample_card['id']}")
    assert response.status_code == 200
    assert response.json()["chinese"] == "你好"


def test_get_flashcard_not_found(client):
    response = client.get("/api/flashcards/9999")
    assert response.status_code == 404


# ── POST /api/flashcards — admin only ────────────────────────────────────────

def test_admin_can_create_flashcard(client, admin_headers):
    response = client.post(
        "/api/flashcards",
        json={"chinese": "谢谢", "pinyin": "xiè xie", "english": "thank you", "category": "Greetings"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["chinese"] == "谢谢"


def test_user_cannot_create_flashcard(client, user_headers):
    response = client.post(
        "/api/flashcards",
        json={"chinese": "谢谢", "pinyin": "xiè xie", "english": "thank you", "category": "Greetings"},
        headers=user_headers,
    )
    assert response.status_code == 403


def test_unauthenticated_cannot_create_flashcard(client):
    response = client.post(
        "/api/flashcards",
        json={"chinese": "谢谢", "pinyin": "xiè xie", "english": "thank you", "category": "Greetings"},
    )
    assert response.status_code == 401


# ── PUT /api/flashcards/{id} — admin only ────────────────────────────────────

def test_admin_can_update_flashcard(client, admin_headers, sample_card):
    response = client.put(
        f"/api/flashcards/{sample_card['id']}",
        json={"english": "hi there"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["english"] == "hi there"


def test_user_cannot_update_flashcard(client, user_headers, sample_card):
    response = client.put(
        f"/api/flashcards/{sample_card['id']}",
        json={"english": "hi there"},
        headers=user_headers,
    )
    assert response.status_code == 403


def test_unauthenticated_cannot_update_flashcard(client, sample_card):
    response = client.put(f"/api/flashcards/{sample_card['id']}", json={"english": "hi"})
    assert response.status_code == 401


def test_update_nonexistent_flashcard_returns_404(client, admin_headers):
    response = client.put("/api/flashcards/9999", json={"english": "hi"}, headers=admin_headers)
    assert response.status_code == 404


# ── DELETE /api/flashcards/{id} — admin only ─────────────────────────────────

def test_admin_can_delete_flashcard(client, admin_headers, sample_card):
    response = client.delete(f"/api/flashcards/{sample_card['id']}", headers=admin_headers)
    assert response.status_code == 200
    assert client.get(f"/api/flashcards/{sample_card['id']}").status_code == 404


def test_user_cannot_delete_flashcard(client, user_headers, sample_card):
    response = client.delete(f"/api/flashcards/{sample_card['id']}", headers=user_headers)
    assert response.status_code == 403


def test_unauthenticated_cannot_delete_flashcard(client, sample_card):
    response = client.delete(f"/api/flashcards/{sample_card['id']}")
    assert response.status_code == 401


def test_delete_nonexistent_flashcard_returns_404(client, admin_headers):
    response = client.delete("/api/flashcards/9999", headers=admin_headers)
    assert response.status_code == 404


# ── POST /api/reset — admin only ─────────────────────────────────────────────

def test_admin_can_reset_cards(client, admin_headers, sample_card):
    response = client.post("/api/reset", headers=admin_headers)
    assert response.status_code == 200


def test_user_cannot_reset_cards(client, user_headers):
    response = client.post("/api/reset", headers=user_headers)
    assert response.status_code == 403


def test_unauthenticated_cannot_reset_cards(client):
    response = client.post("/api/reset")
    assert response.status_code == 401


# ── GET /api/categories ───────────────────────────────────────────────────────

def test_get_categories_public(client, sample_card):
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert "Greetings" in response.json()


# ── POST /api/flashcards/{id}/view — auth required ───────────────────────────

def test_authenticated_user_can_record_view(client, user_headers, sample_card):
    response = client.post(f"/api/flashcards/{sample_card['id']}/view", headers=user_headers)
    assert response.status_code == 200


def test_unauthenticated_cannot_record_view(client, sample_card):
    response = client.post(f"/api/flashcards/{sample_card['id']}/view")
    assert response.status_code == 401


def test_record_view_for_nonexistent_card_returns_404(client, user_headers):
    response = client.post("/api/flashcards/9999/view", headers=user_headers)
    assert response.status_code == 404


def test_card_view_appears_in_user_history(client, user_headers, user_token, sample_card):
    client.post(f"/api/flashcards/{sample_card['id']}/view", headers=user_headers)
    me = client.get("/api/me", headers=user_headers).json()
    assert len(me["card_views"]) == 1
    assert me["card_views"][0]["card_chinese"] == "你好"


def test_multiple_views_are_all_recorded(client, user_headers, sample_card):
    for _ in range(3):
        client.post(f"/api/flashcards/{sample_card['id']}/view", headers=user_headers)
    me = client.get("/api/me", headers=user_headers).json()
    assert len(me["card_views"]) == 3


# ── PUT /api/flashcards/{id}/studied — auth required ─────────────────────────

def test_user_can_mark_card_studied(client, user_headers, sample_card):
    response = client.put(
        f"/api/flashcards/{sample_card['id']}/studied",
        json={"studied": True},
        headers=user_headers,
    )
    assert response.status_code == 200


def test_studied_state_is_per_user(client, admin_headers, user_headers, sample_card):
    # user marks it studied
    client.put(f"/api/flashcards/{sample_card['id']}/studied", json={"studied": True}, headers=user_headers)
    # user sees studied=True
    user_cards = client.get("/api/flashcards", headers=user_headers).json()
    user_card = next(c for c in user_cards if c["id"] == sample_card["id"])
    assert user_card["studied"] is True
    # admin sees studied=False (their own progress untouched)
    admin_cards = client.get("/api/flashcards", headers=admin_headers).json()
    admin_card = next(c for c in admin_cards if c["id"] == sample_card["id"])
    assert admin_card["studied"] is False


def test_mark_studied_then_unmark(client, user_headers, sample_card):
    client.put(f"/api/flashcards/{sample_card['id']}/studied", json={"studied": True}, headers=user_headers)
    client.put(f"/api/flashcards/{sample_card['id']}/studied", json={"studied": False}, headers=user_headers)
    cards = client.get("/api/flashcards", headers=user_headers).json()
    card = next(c for c in cards if c["id"] == sample_card["id"])
    assert card["studied"] is False


def test_mark_studied_unauthenticated_returns_401(client, sample_card):
    response = client.put(f"/api/flashcards/{sample_card['id']}/studied", json={"studied": True})
    assert response.status_code == 401
