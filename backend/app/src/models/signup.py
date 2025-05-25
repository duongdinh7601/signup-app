from datetime import datetime

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
    def __init__(self, name: str, max_attendees=None):
        self.name = name
        # set max number of attendees for event
        self.max_attendees = max_attendees
        # list of SignUp objects (users)
        self.signups = []

    # adding signups to list
    def add_signup(self, user_id):
        signup = SignUp(user_id)
        self.signups.append(signup)
        return signup