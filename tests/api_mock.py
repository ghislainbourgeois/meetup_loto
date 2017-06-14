class FakeApi:
    def get_rsvps(self, meetup_name, event_id):
        return [{'member': {'id':n}} for n in range(1, 11)]
