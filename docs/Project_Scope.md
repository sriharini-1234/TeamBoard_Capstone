# Project Scope – TeamBoard

## Problem statement
Small teams need a simple shared place to track work tickets and see progress. TeamBoard provides a role-aware ticket board with live change notifications.

## MVP user stories
- As any signed-in user, I want to view the ticket board.
- As a member or admin, I want to create a ticket.
- As a member or admin, I want to update a ticket's title, description, priority and status.
- As an admin, I want to delete a ticket.
- As any signed-in user, I want to see status counts.
- As any signed-in user, I want the board to refresh when another user changes a ticket.

## Roles
- Viewer: read-only.
- Member: view, create and update.
- Admin: view, create, update and delete.

## Acceptance criteria
1. Requests without a valid bearer token to protected ticket routes return 401.
2. Viewer create/update/delete attempts are rejected with 403.
3. Member can create and update tickets but cannot delete.
4. Admin can delete tickets.
5. A title shorter than 3 characters is rejected.
6. The board shows Todo, In progress and Done counts.
7. Ticket changes broadcast a WebSocket event.

## Out of scope
Comments, file attachments, notifications, search, persistent database, Redis, Docker and production deployment.
