# TeamBoard Mentor Submission Guide

This guide explains the project, how to run and demonstrate it, what to test, and what to submit. It is written for a local Windows setup.

## 1. Project summary

TeamBoard is a web application for tracking team work as tickets. Users sign in with a role, then view tickets arranged by status. Members and admins can create and update tickets; only admins can delete them.

### Technologies

- **Frontend:** React and TypeScript. Vite runs the frontend during development. Node.js and npm are tools used to install packages and run Vite; Node.js is not the UI framework.
- **Backend:** Python and FastAPI, with Pydantic request validation.
- **Authentication and permissions:** JWT bearer tokens and backend-enforced roles.
- **Live updates:** WebSockets notify connected clients when tickets change.
- **Caching:** Ticket-list ETags and a process-local, time-limited statistics cache.
- **Automated tests:** pytest and FastAPI's test client.

### Main folders

| Path | Contents |
|---|---|
| `frontend/src/` | React application and styles |
| `backend/app/` | FastAPI app, authentication, ticket routes, cache, and WebSockets |
| `backend/tests/` | Automated backend tests |
| `docs/` | Scope, API, implementation, testing, and submission documents |

## 2. Functional requirements and roles

| Role | View tickets | Create tickets | Update tickets | Delete tickets |
|---|---:|---:|---:|---:|
| Viewer | Yes | No | No | No |
| Member | Yes | Yes | Yes | No |
| Admin | Yes | Yes | Yes | Yes |

Tickets have a title, description, priority, owner, and status. The board displays **To do**, **In progress**, and **Done** counts.

## 3. Prepare the development environment

Install Python 3.10 or newer and Node.js 18 or newer. npm is included with Node.js. In PowerShell, check the installations:

```powershell
py --version
node --version
npm --version
```

Open the project folder in VS Code. The example commands below use the path from this project; change it if you saved the project elsewhere.

## 4. Install and start the backend

Open a PowerShell terminal in VS Code and run these commands from the project root:

```powershell
cd "C:\Users\<your-name>\Desktop\TeamBoard_Capstone_Project\backend"
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
$env:FRONTEND_ORIGIN = "http://localhost:5174"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Replace `<your-name>` with your Windows account folder name. The virtual environment and package installation are normally needed only once. Keep this terminal open while using the app.

Expected local URLs:

- API: `http://127.0.0.1:8001`
- Interactive Swagger API page: `http://127.0.0.1:8001/docs`
- Health check: `http://127.0.0.1:8001/health`

## 5. Install and start the frontend

Open a **second** PowerShell terminal. Run:

```powershell
cd "C:\Users\<your-name>\Desktop\TeamBoard_Capstone_Project\frontend"
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

Keep this terminal open too. Open `http://localhost:5174` in a browser. The explicit port avoids opening a different app that may already be using port 5173.

The backend's `FRONTEND_ORIGIN` value must match the frontend URL exactly. If you choose a different port, stop the backend with Ctrl+C, set the environment variable to that origin, and restart the backend.

## 6. Demonstrate the application

Use the following demo accounts:

| Role | Username | Password |
|---|---|---|
| Viewer | `viewer` | `viewer123` |
| Member | `member` | `member123` |
| Admin | `admin` | `admin123` |

Suggested demonstration:

1. Open the frontend and sign in as `member`.
2. Create a ticket with a title of at least three characters.
3. Change the ticket's status and show the board counts update.
4. Sign out and sign in as `viewer`; show that write controls are unavailable.
5. Sign out and sign in as `admin`; demonstrate deleting a ticket.
6. Open Swagger at `http://127.0.0.1:8001/docs` and show the API routes.
7. If demonstrating live updates, use two browser windows and make a ticket change in one.

## 7. Run automated tests

With the backend virtual environment active, open a terminal in the `backend` folder and run:

```powershell
python -m pytest -q
```

Save the actual command output or take a screenshot of the terminal for submission. Do not report a test as passed unless you ran it and observed a passing result. The current automated test file checks the health endpoint, member ticket creation versus viewer denial, and admin deletion. Other behaviors can be demonstrated manually or covered by future tests.

## 8. Suggested evidence to submit

Capture genuine screenshots from your own run. Avoid including passwords other than the documented demo credentials, access tokens, or the contents of `.env`.

1. VS Code showing the project folders.
2. Backend terminal showing Uvicorn running on port 8001.
3. Frontend terminal showing Vite running on port 5174.
4. TeamBoard sign-in page.
5. Member board with a created ticket.
6. Viewer account showing read-only access.
7. Admin account demonstrating deletion.
8. Swagger page showing the API routes.
9. Terminal with the actual pytest results.
10. Optional: two browser windows demonstrating a live ticket update.

Use the [Testing Report](Testing_Report.md) to record the test command, date, actual result, and any failures. The Swagger URL and frontend URL are local addresses; they are not public links and only work while the corresponding local server is running.

## 9. Documentation to include

- [Project scope](Project_Scope.md): problem statement, user stories, roles, and acceptance criteria.
- [API documentation](API_Documentation.md): available endpoints and response codes.
- [Implementation report](Implementation_Report.md): architecture and implementation choices.
- [Testing report](Testing_Report.md): automated tests and observed results.
- This guide: setup, demonstration, and submission checklist.

## 10. Known limitations

- Tickets are held in memory and disappear when the backend restarts.
- Demo users and passwords are for local learning only.
- The frontend stores its demo access token in browser local storage.
- The WebSocket and statistics cache are process-local.
- This project is not configured for production deployment.
- Never commit `backend/.env`; it contains local configuration.

## 11. Optional: update the GitHub repository

From the project root, check and review the files before publishing:

```powershell
git status
git add README.md docs/
git status
git commit -m "Add mentor submission documentation"
git push
```

Confirm that `.env`, the Python virtual environment, and `node_modules` are not staged before committing.
