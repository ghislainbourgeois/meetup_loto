import requests


class MeetupApi:
    def get_rsvps(self, meetup_name, event_id):
        r = requests.get("https://api.meetup.com/%s/events/%s/rsvps" % (meetup_name, event_id))
        return r.json()
