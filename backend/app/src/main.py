from fastapi import FastAPI, Request, Form, HTTPException #web framework
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.signup import Event
from logic.sort_logic import get_attendees_and_waitlist
from typing import Optional

# set up FastAPI app and template system
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory store for now
events = {} # stores all events using their ID as key
event_id_counter = 1 # tracks the next event's ID

# route: homepage
# displays all events by passing the events dictionary to the template
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "events": events})

# route: event creation page
@app.get("/create", response_class=HTMLResponse)
def create_event_form(request: Request):
    return templates.TemplateResponse("create_event.html", {"request": request})

# route: event creation handler
# receives form data from events creation page and allows user to input event information
# creates a new event, automatically signs up the organizer, stores new event in events dictionary and redirects to homepage
@app.post("/create")
def create_event(name: str = Form(...), organizer_name: str = Form(...), date_start: Optional[str] = Form(None), date_end: Optional[str] = Form(None), time_start: Optional[str] = Form(None), time_end: Optional[str] = Form(None), max_attendees: Optional[str] = Form(None), cost: Optional[str] = Form(None)):
    global event_id_counter

    max_attendees_int = int(max_attendees) if max_attendees and max_attendees.strip() != '0' else None

    event = Event(name=name, date_start=date_start if date_start and date_start != "TBD" else None, date_end=date_end if date_end and date_end != "" else None, time_start=time_start if time_start and time_start != "TBD" else None, time_end=time_end if time_end and time_end != "" else None, max_attendees=max_attendees_int, cost=cost or "Free")
    event.add_signup(organizer_name)
    events[event_id_counter] = event
    event_id_counter += 1
    return RedirectResponse(url="/", status_code=302)

# route: signup page for an event
@app.get("/signup/{event_id}", response_class=HTMLResponse)
def signup_form(request: Request, event_id: int):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found") # if event doesn't exist/ended
    event = events[event_id]
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "event_id": event_id,
        "event": event,
    })

# route: signup submission handler
# adds user to the event's signup list then redirects to the event detail page
@app.post("/signup/{event_id}")
def signup(event_id: int, user_name: str = Form(...)):
    event = events[event_id]
    event.add_signup(user_name)
    return RedirectResponse(url=f"/event/{event_id}", status_code=302)

# route: event details page
# shows attendees and those waitlisted
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