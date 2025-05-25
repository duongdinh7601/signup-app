# getter methods

def get_sorted_signups(signups):
    # first come first serve
    return sorted(signups, key=lambda s: s.signup_time)

def get_attendees_and_waitlist(signups, max_attendees):
    sorted_signups = get_sorted_signups(signups)

    # everyone gets in if no limit
    if max_attendees is None:
        return sorted_signups, []
    
    return sorted_signups[:max_attendees], sorted_signups[max_attendees:]