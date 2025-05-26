from datetime import datetime, date, time

# class for a user who joins a list
class SignUp:
    def __init__(self, user_id, signup_time=None):
        self.user_id = user_id

        # timestamp of signup
        self.signup_time = signup_time or datetime.now()

    def __repr__(self):
        return f"<User {self.user_id} | SignUp: {self.signup_time.time()}>"
    
# class for managing the event and signups
class Event:
    def __init__(self, name: str, date_start=None, date_end=None, time_start=None, time_end=None, max_attendees=None, cost=None):
        self.name = name
        #set date and time of event
        # convert string to date object or None
        self.date_start = datetime.strptime(date_start, "%Y-%m-%d").date() if date_start else None
        self.date_end = datetime.strptime(date_end, "%Y-%m-%d").date() if date_end else None

        #convert string like '7:00AM' to time object or None
        self.time_start = datetime.strptime(time_start, "%I:%M %p").time() if time_start and time_start != "TBD" else None
        self.time_end = datetime.strptime(time_end, "%I:%M %p").time() if time_end else None
        
        # set max number of attendees for event
        self.max_attendees = max_attendees
        # set cost per attendee
        self.cost = cost
        # list of SignUp objects (users)
        self.signups = []

    # adding signups to list
    def add_signup(self, user_id):
        signup = SignUp(user_id)
        self.signups.append(signup)
        return signup