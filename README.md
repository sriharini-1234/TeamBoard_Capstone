# TeamBoard

TeamBoard is a small web app for organizing a team's work as tickets. Sign in, view the ticket board, and—depending on your account—create, update, or delete tickets.

This project is a learning/demo app built with **React and TypeScript** in the browser and **FastAPI and Python** on the server.

## Project links

- [Project scope](docs/Project_Scope.md) — what the app is meant to do.
- [API documentation](docs/API_Documentation.md) — how the frontend and backend communicate.
- [Implementation report](docs/Implementation_Report.md) — how the project was built.
- [TeamBoard results and test cases](docs/Testing_Report.md) — test cases and space to record test results.
- [Mentor submission guide](docs/Mentor_Submission_Guide.md) — setup, demo, testing, and evidence checklist.
- [Backend results (interactive API / Swagger)](http://127.0.0.1:8001/docs) — available while the backend is running locally.
- [Backend source code](backend/app/)
- [Frontend source code](frontend/src/)

## What you can do

- Sign in as a viewer, member, or admin.
- View tickets organized into **To do**, **In progress**, and **Done**.
- Create tickets and update their status if your role allows it.
- Delete tickets as an admin.
- See status counts and receive live updates while the app is open.

## What you need

Install these before starting:

- **Python 3.10 or newer**
- **Node.js 18 or newer** (npm is included with Node.js)
- **Git**, if you want to clone the project or push it to GitHub

To check that Python and Node.js are installed, open PowerShell and run:

```powershell
py --version
node --version
npm --version
```

## Start TeamBoard on Windows

The backend and frontend run in **two separate PowerShell terminals**. Keep both terminals open while using the app.

### 1. Start the backend

Open the first PowerShell terminal and go to the backend folder:

```powershell
cd "C:\Users\<your-name>\Desktop\TeamBoard_Capstone_Project\backend"
```

Replace `<your-name>` with your Windows account folder name. If your project is in a different location, use that location instead.

The next commands create a Python virtual environment, install the backend packages, and create your local settings file. Run the environment and install commands the first time you set up the project:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` from the example if it does not already exist:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Set the address the backend should allow for TeamBoard's frontend, then start the API:

```powershell
$env:FRONTEND_ORIGIN = "http://127.0.0.1:5174"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Leave this terminal running. The backend is available at [http://127.0.0.1:8001](http://127.0.0.1:8001), and its interactive API page is [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs).

### 2. Start the frontend

Open a **second** PowerShell terminal and go to the frontend folder:

```powershell
cd "C:\Users\<your-name>\Desktop\TeamBoard_Capstone_Project\frontend"
```

Install frontend packages the first time, then start the development server:

```powershell
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

Open TeamBoard at [http://127.0.0.1:5174](http://127.0.0.1:5174). Port `5173` may show a different app if another development server is using it. If Vite selects a different port because `5174` is busy, set `FRONTEND_ORIGIN` in the backend terminal to the exact URL Vite prints and restart the backend.

### 3. Sign in

Use one of these demo accounts:

| Role | Username | Password | Permissions |
|---|---|---|---|
| Viewer | `viewer` | `viewer123` | View tickets |
| Member | `member` | `member123` | View, create, and update tickets |
| Admin | `admin` | `admin123` | View, create, update, and delete tickets |

## If something goes wrong

### PowerShell says script execution is disabled

In the backend terminal, allow scripts for that terminal only, then activate the virtual environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### “Address already in use” or “Only one usage of each socket address”

That port is already being used, often by another copy of TeamBoard. Do not start a second backend on port `8001`. Stop the existing server with **Ctrl+C** in its terminal, or keep using the server that is already running.

If Vite reports that port `5173` is busy, it may start the frontend on `5174` instead. Set `FRONTEND_ORIGIN` in the backend terminal to the exact frontend URL Vite printed, for example:

```powershell
$env:FRONTEND_ORIGIN = "http://127.0.0.1:5174"
```

Then restart the backend so it reads the new setting.

### The login page says “Failed to fetch”

Make sure the backend terminal still shows Uvicorn running on port `8001`. Also check that `FRONTEND_ORIGIN` matches the frontend URL exactly, including the port. Keep both development-server terminals open.

### Tickets disappear after restarting the backend

That is expected in this demo: tickets are kept in memory and are cleared when the backend restarts.

## Run the backend tests

In a PowerShell terminal, go to the backend folder and activate its virtual environment if it is not already active:

```powershell
cd "C:\Users\<your-name>\Desktop\TeamBoard_Capstone_Project\backend"
.\venv\Scripts\Activate.ps1
python -m pytest -q
```

The test report lists the test cases; run this command to get the results on your computer.

## How the project is organized

```text
TeamBoard_Capstone_Project/
├── backend/
│   ├── app/          Python API and WebSocket code
│   └── tests/        Backend tests
├── docs/             Project, API, implementation, and test reports
├── frontend/
│   └── src/          React application and styles
└── README.md         This guide
```

## API at a glance

The API is served from `http://127.0.0.1:8001`.

| Method | URL path | What it does | Who can use it |
|---|---|---|---|
| `POST` | `/auth/login` | Sign in and receive an access token | Anyone with a demo account |
| `GET` | `/tickets` | List tickets | Signed-in users |
| `POST` | `/tickets` | Create a ticket | Members and admins |
| `PATCH` | `/tickets/{id}` | Update a ticket | Members and admins |
| `DELETE` | `/tickets/{id}` | Delete a ticket | Admins |
| `GET` | `/tickets/stats` | Get ticket counts | Signed-in users |
| `WS` | `/ws/tickets` | Receive live ticket updates | Signed-in users |
| `GET` | `/health` | Check whether the API is running | Anyone |

## Demo limitations

- This is a local learning project, not a production-ready service.
- Tickets are stored in memory and reset when the backend restarts.
- Demo usernames and passwords are included for learning purposes only.
- The frontend stores its demo access token in browser `localStorage`.
- The WebSocket and statistics cache work in the running backend process only.
- Do not publish your local `backend/.env` file or use the demo credentials for a real deployment.
