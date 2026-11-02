# Implementation Report – TeamBoard

## Architecture
The project is a small monorepo containing a React + TypeScript frontend and a FastAPI backend. The frontend calls REST endpoints for ticket data. The backend validates request payloads with Pydantic and checks JWTs for protected routes.

## Main components
- `main.py`: creates the FastAPI application and configures CORS.
- `schemas.py`: request and response models.
- `security.py`: JWT creation, verification and role dependencies.
- `routers/auth.py`: demo login endpoint.
- `routers/tickets.py`: ticket CRUD and statistics.
- `cache.py`: ETag helper and TTL cache.
- `ws.py`: WebSocket connection manager and broadcast endpoint.
- `frontend/src/App.tsx`: login, ticket board and API integration.

## Security model
The backend enforces roles. Hiding a button in the frontend is only a user-interface convenience and is not a security boundary. A viewer's direct write request is rejected by the API.

## Caching and live updates
The ticket list response includes an ETag. Statistics are held in a process-local TTL cache for 30 seconds and cleared after ticket writes. WebSocket events notify connected clients that a ticket changed; clients then reload the list through REST.

## Limitations
The starter uses in-memory storage and hard-coded demo users. It is intended for local learning and capstone demonstration, not production deployment.
