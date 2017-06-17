import re
import tests.context
import unittest
import server
from meetup_api import MeetupApi

class WebMeetupLotoTestCase(unittest.TestCase):

    def setUp(self):
        server.app.testing = True
        server.app.config.update(dict(api=MeetupApi()))
        self.app = server.app.test_client()

    def test_rsvps(self):
        result = self._post_meetup_details("Docker-Montreal", 240672864)
        assert b'Number of participants: 4' in result.data
        assert b'Winning chances: 25.0%' in result.data

    def test_draw_winner(self):
        self._post_meetup_details("Docker-Montreal", 240672864)
        result = self.app.get('/draw')
        assert b"<a href='/draw'>Draw another!</a>" in result.data
        self._assert_valid_draw(result)

    def test_draw_all(self):
        self._post_meetup_details("Docker-Montreal", 240672864)
        self._draw_all()
        result = self.app.get('/draw')
        assert b'Sorry, there are no more participants to draw from' in result.data

    def _draw_all(self):
        for i in range(4):
            result = self.app.get('/draw')
            self._assert_valid_draw(result)

    def _assert_valid_draw(self, result):
        match = re.search('<b>Winner ID: ([0-9]*)</b>', result.data.decode('utf-8'))
        assert match
        assert int(match.group(1)) in range(20000001, 20000005)

    def _post_meetup_details(self, m, e):
        return self.app.post('/query', data=dict(
            meetup_name=m,
            event_id=e
        ), follow_redirects=True)

