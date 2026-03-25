# ni-howl

chinese language flashcard learning application

## problem

helps users learn chinese vocabulary through interactive digital flashcards with character, pinyin and english translations organized by difficulty level

## technical stack

- frontend: react with vite
- styling: tailwind css
- routing: single-page application, no routing library needed
- backend: fastapi
- database: sqlite with sqlalchemy orm
- deployment: docker compose

## features

- create, read, update, delete flashcard operations
- chinese characters with pinyin romanization and english translations
- category organization by hsk levels and topics
- interactive card flip animation
- previous and next navigation between cards
- shuffle functionality for randomized study order
- category filtering in study mode
- category filtering in manage mode
- 50 default flashcards seeded on first launch
- database reset with browser confirmation dialog
- single-page application architecture
- responsive mobile design
- minimal design with red, yellow, black, white color scheme

## project structure

```
ni-howl/
├── backend/
│   ├── app/
│   │   ├── main.py - api endpoints
│   │   ├── models.py - database models
│   │   ├── crud.py - database operations
│   │   ├── database.py - database configuration
│   │   └── seed.py - default flashcard data
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/ - react ui components
│   │   ├── services/ - api client functions
│   │   ├── App.jsx - main application component
│   │   └── App.css - tailwind directives
│   └── Dockerfile
└── docker-compose.yml
```

## setup

```bash
docker-compose up
```

access at <http://localhost:3000>

## challenges

implemented css 3d transforms for card flip animations with react state synchronization. built dual filtering system maintaining separate state for study and manage views to prevent interference. created manual navigation preserving card flip state when moving between cards. developed atomic database reset operation using transaction to delete all records then re-seed defaults ensuring consistency. handled sqlite persistence across container restarts using docker named volumes.
