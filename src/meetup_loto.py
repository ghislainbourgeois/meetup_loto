import random


class Loto:
    def __init__(self, api, meetup_name, event_id):
        self.api = api
        self.meetup_name = meetup_name
        self.event_id = event_id
        self.participants = self._get_participants_member_ids()

    def number_of_participants(self):
        return len(self.participants)

    def current_chances(self):
        return (1.0 / self.number_of_participants()) * 100.0

    def draw(self):
        if (self.number_of_participants() > 0):
            winner = random.choice(self.participants)
            self.participants.remove(winner)
            return winner
        else:
            return 0

    def get_member_name(self, member_id):
        return self.api.get_member_name(self.meetup_name, member_id)

    def get_member_photo_url(self, member_id):
        return self.api.get_member_photo_url(self.meetup_name, member_id)

    def _get_participants_member_ids(self):
        rsvps = self.api.get_rsvps(self.meetup_name, self.event_id)
        return [rsvp['member']['id'] for rsvp in rsvps]
