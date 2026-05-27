# Ni-Howl

A Chinese flashcard study app with role-based access control. Regular users can browse and study flashcards and track their own progress. Admins can manage the flashcard library and all user accounts.

---

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | Python 3.11, FastAPI, SQLAlchemy |
| Database | SQLite (persisted via Docker volume) |
| Auth | JWT (PyJWT, HS256), bcrypt password hashing |
| Containerisation | Docker, Docker Compose |

---

## Running the App

**Prerequisites:** Docker and Docker Compose

```bash
git clone <repo-url>
cd junk-yard
docker compose up --build
```

The app will be available at **http://localhost:3000**

Default accounts:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| amy | 123 | user |
| yunz | meow | user |

**Environment variables**

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | JWT signing secret — change this before deploying |
| `API_HOST` | Backend URL used by the Vite dev proxy |

**Running tests**

```bash
docker compose exec backend python -m pytest tests/ -v
```

---

## Folder Structure

```
junk-yard/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py         # route handlers
│       ├── models.py       # ORM models: User, Flashcard, CardView, UserCardProgress
│       ├── schemas.py      # Pydantic request/response types
│       ├── crud.py         # database query functions
│       ├── auth.py         # JWT, password hashing, FastAPI auth dependencies
│       ├── database.py     # SQLAlchemy engine and session
│       └── seed.py         # default users and flashcard data
│   └── tests/
│       ├── conftest.py         # shared fixtures
│       ├── test_auth.py        # auth and password tests
│       ├── test_flashcards.py  # flashcard CRUD and per-user progress tests
│       └── test_users.py       # user management and access control tests
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── App.jsx                     # root component, global state, navigation
        ├── App.css                     # Tailwind directives and flip animation
        ├── main.jsx
        ├── services/
        │   └── api.js                  # all backend fetch calls
        └── components/
            ├── Login.jsx               # login and register form
            ├── Flashcard.jsx           # flip card component
            ├── FlashcardForm.jsx       # add card modal (admin only)
            ├── CardList.jsx            # manage view card grid
            ├── AdminPanel.jsx          # user list table (admin only)
            ├── UserProfile.jsx         # user detail, history, edit
            └── ChangePasswordForm.jsx  # self-service password change
```

---

## Workload Allocation

### Amy (0melette)
- `backend/app/auth.py` — JWT token creation/decoding, password hashing, `get_current_user`, `require_admin`, `get_optional_user`
- `backend/app/main.py` — `/api/register`, `/api/login`, `/api/me` endpoints
- `backend/app/schemas.py` — `AuthRequest`, `AuthResponse`, `SelfChangePassword`
- `frontend/src/components/Login.jsx` — login and register UI
- `frontend/src/components/UserProfile.jsx` — profile display and practice history
- `frontend/src/components/ChangePasswordForm.jsx` — self-service password change
- `backend/tests/test_auth.py`

### yunz-dev
- `backend/app/models.py` — all ORM models
- `backend/app/crud.py` — all database query functions
- `backend/app/main.py` — flashcard, user management, progress and view endpoints
- `backend/app/seed.py`
- `frontend/src/App.jsx` — root component, search and filter logic
- `frontend/src/services/api.js`
- `frontend/src/components/CardList.jsx`
- `frontend/src/components/FlashcardForm.jsx`
- `frontend/src/components/Flashcard.jsx`
- `frontend/src/components/AdminPanel.jsx`
- `frontend/src/components/UserProfile.jsx` — admin edit form section
- `backend/tests/conftest.py`, `test_flashcards.py`, `test_users.py`
