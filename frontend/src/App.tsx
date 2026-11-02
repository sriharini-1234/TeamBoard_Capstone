import { useCallback, useEffect, useMemo, useState } from 'react';

const API = 'http://127.0.0.1:8001';
type Role = 'viewer' | 'member' | 'admin';
type Ticket = {id:number; title:string; description:string; priority:'low'|'medium'|'high'; status:'todo'|'doing'|'done'; owner:string};
type Session = {username:string; role:Role; access_token:string};

export default function App() {
  const [session, setSession] = useState<Session | null>(() => {
    const raw = localStorage.getItem('teamboard_session'); return raw ? JSON.parse(raw) : null;
  });
  const [username,setUsername] = useState('member');
  const [password,setPassword] = useState('member123');
  const [tickets,setTickets] = useState<Ticket[]>([]);
  const [title,setTitle] = useState('');
  const [description,setDescription] = useState('');
  const [priority,setPriority] = useState<'low'|'medium'|'high'>('medium');
  const [error,setError] = useState('');
  const [notice,setNotice] = useState('');
  const [loading,setLoading] = useState(false);

  const headers = useMemo((): Record<string, string> => {
  const requestHeaders: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (session?.access_token) {
    requestHeaders["Authorization"] = `Bearer ${session.access_token}`;
  }

  return requestHeaders;
}, [session]);

  const loadTickets = useCallback(async () => {
    if (!session) return;
    try {
      const response = await fetch(`${API}/tickets`, {headers});
      if (!response.ok) throw new Error((await response.json()).detail || 'Could not load tickets');
      setTickets(await response.json());
    } catch(e) { setError(e instanceof Error ? e.message : 'Network error'); }
  },[session,headers]);

  useEffect(() => { loadTickets(); },[loadTickets]);

  useEffect(() => {
    if (!session) return;
    const socket = new WebSocket('ws://127.0.0.1:8001/ws/tickets');
    socket.onopen = () => socket.send(JSON.stringify({token:session.access_token}));
    socket.onmessage = (event) => { const msg = JSON.parse(event.data); if (msg.type === 'ready' || msg.type?.startsWith('ticket.')) loadTickets(); };
    return () => socket.close();
  },[session,loadTickets]);

  async function login(e: React.FormEvent) {
    e.preventDefault(); setError('');
    try {
      const res = await fetch(`${API}/auth/login`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});
      const data = await res.json(); if (!res.ok) throw new Error(data.detail || 'Login failed');
      setSession(data); localStorage.setItem('teamboard_session',JSON.stringify(data));
    } catch(e) { setError(e instanceof Error ? e.message : 'Login failed'); }
  }


  async function createTicket(e: React.FormEvent) {
    e.preventDefault(); setError(''); setNotice('');
    if (title.trim().length < 3) { setError('Title must contain at least 3 characters.'); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API}/tickets`,{method:'POST',headers,body:JSON.stringify({title,description,priority})});
      const data = await res.json(); if (!res.ok) throw new Error(data.detail || 'Could not create ticket');
      setTitle(''); setDescription(''); setNotice('Ticket created successfully.'); await loadTickets();
    } catch(e) { setError(e instanceof Error ? e.message : 'Create failed'); }
    finally { setLoading(false); }
  }

  async function updateTicket(id:number, patch:Partial<Ticket>) {
    setError('');
    try {
      const res = await fetch(`${API}/tickets/${id}`,{method:'PATCH',headers,body:JSON.stringify(patch)});
      const data = await res.json(); if (!res.ok) throw new Error(data.detail || 'Update failed');
      setTickets(old => old.map(t => t.id === id ? data : t));
    } catch(e) { setError(e instanceof Error ? e.message : 'Update failed'); }
  }

  async function deleteTicket(id:number) {
    if (!confirm('Delete this ticket?')) return;
    try {
      const res = await fetch(`${API}/tickets/${id}`,{method:'DELETE',headers});
      if (!res.ok) throw new Error((await res.json()).detail || 'Delete failed');
      setTickets(old => old.filter(t => t.id !== id)); setNotice('Ticket deleted.');
    } catch(e) { setError(e instanceof Error ? e.message : 'Delete failed'); }
  }

  function logout() { localStorage.removeItem('teamboard_session'); setSession(null); setTickets([]); }

  const counts = {todo:tickets.filter(t=>t.status==='todo').length,doing:tickets.filter(t=>t.status==='doing').length,done:tickets.filter(t=>t.status==='done').length};
  if (!session) return <main className="login-shell"><form className="login-card" onSubmit={login}><div className="brand-mark">TB</div><p className="eyebrow">TEAM WORKSPACE</p><h1>Welcome to TeamBoard</h1><p className="muted">Sign in to manage your team's tickets.</p><label>Username<input value={username} onChange={e=>setUsername(e.target.value)} /></label><label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} /></label>{error && <p className="error">{error}</p>}<button className="primary full">Sign in</button><div className="demo-users"><b>Demo accounts</b><span>viewer / viewer123</span><span>member / member123</span><span>admin / admin123</span></div></form></main>;

  return <main className="app-shell"><header className="topbar"><div className="brand"><div className="brand-mark small">TB</div><span>TeamBoard</span></div><div className="user-area"><span className="role-pill">{session.role}</span><span>{session.username}</span><button className="ghost" onClick={logout}>Log out</button></div></header><section className="content"><div className="page-heading"><div><p className="eyebrow">WORKSPACE / TICKETS</p><h1>Team ticket board</h1><p className="muted">Plan work, track progress and keep everyone aligned.</p></div><button className="ghost" onClick={loadTickets}>↻ Refresh</button></div>
    <div className="stats"><div className="stat"><span>To do</span><strong>{counts.todo}</strong></div><div className="stat"><span>In progress</span><strong>{counts.doing}</strong></div><div className="stat"><span>Completed</span><strong>{counts.done}</strong></div><div className="stat"><span>Total tickets</span><strong>{tickets.length}</strong></div></div>
    {error && <div className="alert error">{error}</div>}{notice && <div className="alert success">{notice}</div>}
    {session.role !== 'viewer' && <form className="create-panel" onSubmit={createTicket}><div><h2>Create a ticket</h2><p className="muted">Add a task for your team.</p></div><div className="form-grid"><label>Title<input placeholder="e.g. Prepare release notes" value={title} onChange={e=>setTitle(e.target.value)} /></label><label>Priority<select value={priority} onChange={e=>setPriority(e.target.value as any)}><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option></select></label><label className="wide">Description<textarea placeholder="Add details (optional)" value={description} onChange={e=>setDescription(e.target.value)} /></label><div className="wide"><button className="primary" disabled={loading}>{loading?'Creating...':'＋ Create ticket'}</button></div></div></form>}
    <div className="board">{(['todo','doing','done'] as const).map(status=><section className="column" key={status}><div className="column-heading"><h2>{status==='todo'?'To do':status==='doing'?'In progress':'Done'}</h2><span>{counts[status]}</span></div>{tickets.filter(t=>t.status===status).map(ticket=><article className="ticket" key={ticket.id}><div className="ticket-top"><span className={`priority ${ticket.priority}`}>{ticket.priority}</span><span className="ticket-id">#{ticket.id}</span></div><h3>{ticket.title}</h3>{ticket.description && <p>{ticket.description}</p>}<div className="ticket-footer"><span>By {ticket.owner}</span>{session.role!=='viewer' && <select aria-label="Change status" value={ticket.status} onChange={e=>updateTicket(ticket.id,{status:e.target.value as Ticket['status']})}><option value="todo">To do</option><option value="doing">In progress</option><option value="done">Done</option></select>}{session.role==='admin' && <button className="delete" onClick={()=>deleteTicket(ticket.id)}>Delete</button>}</div></article>)}{tickets.filter(t=>t.status===status).length===0 && <p className="empty">No tickets yet</p>}</section>)}</div>
    <p className="footer-note">Live updates enabled · Changes from other signed-in users appear automatically.</p></section></main>;
}
