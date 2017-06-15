class FakeApi:
    def get_rsvps(self, meetup_name, event_id):
        return [{'member': {'id':n}} for n in range(1, 11)]

    def get_member_name(self, meetup_name, member_id):
        return "John Doe"

    def get_member_photo_url(self, meetup_name, member_id):
        return "https://upload.wikimedia.org/wikipedia/commons/0/09/Man_Silhouette.png"
