# TeamBoard – Team Ticket Management Capstone

A learning capstone based on the uploaded Capstone Build module. It demonstrates a React + TypeScript frontend and FastAPI backend with JWT authentication, server-enforced roles, ticket CRUD, ETag responses, a small TTL statistics cache, and WebSocket notifications.

## Requirements
- Python 3.10+
- Node.js 18+
- npm

## 1. Run the backend (Windows PowerShell)

```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

API: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 2. Run the frontend (new terminal)

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally http://localhost:5173.

## Demo login accounts
| Role | Username | Password |
|---|---|---|
| Viewer | viewer | viewer123 |
| Member | member | member123 |
| Admin | admin | admin123 |

## API endpoints
| Method | Path | Minimum role | Purpose |
|---|---|---|---|
| POST | /auth/login | Public | Login and receive JWT |
| GET | /tickets | Viewer | List tickets (ETag) |
| POST | /tickets | Member | Create ticket |
| PATCH | /tickets/{id} | Member | Update ticket |
| DELETE | /tickets/{id} | Admin | Delete ticket |
| GET | /tickets/stats | Viewer | Status counts (TTL cache) |
| WS | /ws/tickets | Viewer | Live change notifications |
| GET | /health | Public | Health check |

## 3. Run backend tests

From the `backend` folder:
```powershell
pytest -q
```

## Important learning/demo limitations
- This starter uses in-memory ticket storage. Tickets reset when the backend restarts.
- Demo accounts and passwords are hard-coded for local learning only.
- The frontend stores the demo access token in localStorage for simplicity.
- The WebSocket is a single-process demo. It sends event notifications; the browser reloads the ticket list through REST.
- The TTL cache is process-local. Redis, PostgreSQL persistence, Docker, production-grade password hashing, refresh tokens, and deployment are not included in this starter.
- Change the secret and replace demo authentication/storage before any real deployment.

## Suggested screenshot evidence
1. VS Code project structure.
2. Backend running in terminal.
3. Swagger `/docs`.
4. Login screen with demo accounts visible.
5. Member dashboard and ticket creation.
6. Ticket board showing Todo / In progress / Done.
7. Viewer account showing read-only access.
8. Member trying DELETE in Swagger and receiving 403.
9. Admin deleting a ticket.
10. Pytest results.
11. Two browser windows showing a WebSocket-driven update.

## Module mapping
- Scoping and acceptance criteria: README and endpoint contract.
- Backend/frontend layout and vertical slice: `backend/app` and `frontend/src`.
- Authentication integration: `auth.py` and `security.py`.
- RBAC: `require_role()` on backend routes and role-specific frontend controls.
- ETag: `GET /tickets`.
- TTL cache: `GET /tickets/stats`.
- WebSocket: `/ws/tickets` and frontend socket effect.
- Testing: `backend/tests/test_api.py`.
