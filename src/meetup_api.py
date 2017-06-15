import requests


silhouette = "https://upload.wikimedia.org/wikipedia/commons/0/09/Man_Silhouette.png"

class MeetupApi:
    def get_rsvps(self, meetup_name, event_id):
        r = requests.get("https://api.meetup.com/%s/events/%s/rsvps" % (meetup_name, event_id))
        return r.json()

    def get_member_name(self, meetup_name, member_id):
        r = requests.get("https://api.meetup.com/%s/members/%d" % (meetup_name, member_id))
        return r.json().get('name', "")

    def get_member_photo_url(self, meetup_name, member_id):
        r = requests.get("https://api.meetup.com/%s/members/%d" % (meetup_name, member_id))
        return r.json().get('photo', dict()).get('highres_link', silhouette)
