# TeamBoard API Documentation

Base URL: `http://127.0.0.1:8001`

## Authentication
`POST /auth/login`
```json
{"username":"member","password":"member123"}
```
Returns an access token and role. Send it on protected requests as:
`Authorization: Bearer <access_token>`

## Ticket endpoints
- `GET /tickets` – authenticated viewer or higher; returns ticket list and ETag.
- `POST /tickets` – member or admin; body: `{"title":"Fix login","description":"","priority":"medium"}`.
- `PATCH /tickets/{id}` – member or admin; send only fields to change, such as `{"status":"doing"}`.
- `DELETE /tickets/{id}` – admin only; returns 204.
- `GET /tickets/stats` – authenticated; returns `{"todo":0,"doing":0,"done":0}`.
- `WS /ws/tickets` – connect, then send first JSON message `{"token":"<access_token>"}`. Server sends `{"type":"ready"}` and later event messages such as `{"type":"ticket.updated","id":1}`.

## Common status codes
- 200: successful read/update.
- 201: ticket created.
- 204: ticket deleted.
- 401: missing, invalid or expired token.
- 403: authenticated user lacks permission.
- 404: ticket does not exist.
- 422: request validation failed.
