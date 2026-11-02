from fastapi import APIRouter, Depends, HTTPException, Request, Response
from ..schemas import TicketCreate, TicketUpdate, TicketOut, TicketStats
from ..security import User, current_user, require_role
from ..cache import TTLCache, make_etag
from ..ws import manager

router = APIRouter()
DB: dict[int, TicketOut] = {}
stats_cache = TTLCache(ttl=30)

async def changed(kind: str, ticket_id: int):
    stats_cache.clear()
    await manager.broadcast({"type": kind, "id": ticket_id})

@router.get("", response_model=list[TicketOut])
def list_tickets(request: Request, response: Response, user: User = Depends(current_user)):
    items = [item.model_dump() for item in DB.values()]
    etag = make_etag(items)
    headers = {"ETag": etag, "Cache-Control": "private, no-cache"}
    sent = request.headers.get("if-none-match")
    if sent and sent.strip() == etag:
        return Response(status_code=304, headers=headers)
    response.headers.update(headers)
    return items

@router.post("", response_model=TicketOut, status_code=201)
async def create_ticket(data: TicketCreate, user: User = Depends(require_role("member"))):
    ticket_id = max(DB, default=0) + 1
    ticket = TicketOut(id=ticket_id, status="todo", owner=user.username, **data.model_dump())
    DB[ticket_id] = ticket
    await changed("ticket.created", ticket_id)
    return ticket

@router.patch("/{ticket_id}", response_model=TicketOut)
async def update_ticket(ticket_id: int, data: TicketUpdate, user: User = Depends(require_role("member"))):
    ticket = DB.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    updates = data.model_dump(exclude_unset=True)
    DB[ticket_id] = ticket.model_copy(update=updates)
    await changed("ticket.updated", ticket_id)
    return DB[ticket_id]

@router.delete("/{ticket_id}", status_code=204)
async def delete_ticket(ticket_id: int, user: User = Depends(require_role("admin"))):
    if ticket_id not in DB:
        raise HTTPException(status_code=404, detail="Ticket not found")
    del DB[ticket_id]
    await changed("ticket.deleted", ticket_id)
    return Response(status_code=204)

@router.get("/stats", response_model=TicketStats)
def ticket_stats(user: User = Depends(current_user)):
    cached = stats_cache.get("stats")
    if cached is not None:
        return cached
    counts = {"todo": 0, "doing": 0, "done": 0}
    for ticket in DB.values():
        counts[ticket.status] += 1
    stats_cache.set("stats", counts)
    return counts
