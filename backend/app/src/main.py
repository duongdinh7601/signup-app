from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.signup import Event
from logic.sort_logic import get_attendees_and_waitlist
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory store for now
events = {}
event_id_counter = 1

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "events": events})

@app.get("/create", response_class=HTMLResponse)
def create_event_form(request: Request):
    return templates.TemplateResponse("create_event.html", {"request": request})

@app.post("/create")
def create_event(name: str = Form(...), max_attendees: Optional[int] = Form(...), organizer_name: str = Form(...)):
    global event_id_counter
    if max_attendees == 0:
        max_attendees = None
    event = Event(name=name, max_attendees=max_attendees)
    event.add_signup(organizer_name)
    events[event_id_counter] = event
    event_id_counter += 1
    return RedirectResponse(url="/", status_code=302)

@app.get("/signup/{event_id}", response_class=HTMLResponse)
def signup_form(request: Request, event_id: int):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    event = events[event_id]
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "event_id": event_id,
        "event": event,
    })

@app.post("/signup/{event_id}")
def signup(event_id: int, user_name: str = Form(...)):
    event = events[event_id]
    event.add_signup(user_name)
    return RedirectResponse(url=f"/event/{event_id}", status_code=302)

@app.get("/event/{event_id}", response_class=HTMLResponse)
def show_event(request: Request, event_id: int):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event = events[event_id]
    attendees, waitlist = get_attendees_and_waitlist(event.signups, event.max_attendees)
    return templates.TemplateResponse("event_list.html", {
        "request": request,
        "event": event,
        "attendees": attendees,
        "waitlist": waitlist
    })