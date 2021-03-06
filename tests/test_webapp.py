import re
import tests.context
import unittest
import server
from tests.api_mock import FakeApi

class WebMeetupLotoTestCase(unittest.TestCase):

    def setUp(self):
        server.app.testing = True
        server.app.config.update(dict(api=FakeApi()))
        self.app = server.app.test_client()

    def test_index(self):
        result = self.app.get('/')
        assert b'Meetup Loto!' in result.data
        assert b'Meetup Details' in result.data
        assert b'Meetup Name:' in result.data
        assert b'Event ID:' in result.data
        assert b'Submit' in result.data

    def test_malicious_post(self):
        result = self._post_meetup_details(";DROP DATABASE", "%00")
        assert b'Invalid characters' in result.data

    def test_valid_meetup(self):
        result = self._post_meetup_details("Docker-Montreal", 240672864)
        assert b'Number of participants: 10' in result.data
        assert b'Winning chances: 10.0%' in result.data
        assert b'Draw a Winner!' in result.data

    def test_draw_winner(self):
        self._post_meetup_details("Docker-Montreal", 240672864)
        result = self.app.get('/draw')
        assert b'Winner is...' in result.data
        assert b"<b>Winner's Name: John Doe</b>" in result.data
        assert b'<img height=500 width=500 src="https://upload.wikimedia.org/wikipedia/commons/0/09/Man_Silhouette.png" />' in result.data
        assert b"<a href='/draw'>Draw another!</a>" in result.data
        self._assert_valid_draw(result)

    def test_draw_all(self):
        self._post_meetup_details("Docker-Montreal", 240672864)
        self._draw_all()
        result = self.app.get('/draw')
        assert b'Sorry, there are no more participants to draw from' in result.data

    def _draw_all(self):
        for i in range(10):
            result = self.app.get('/draw')
            self._assert_valid_draw(result)

    def _assert_valid_draw(self, result):
        match = re.search('<b>Winner ID: ([0-9]*)</b>', result.data.decode('utf-8'))
        assert match
        assert int(match.group(1)) in range(1, 11)

    def _post_meetup_details(self, m, e):
        return self.app.post('/query', data=dict(
            meetup_name=m,
            event_id=e
        ), follow_redirects=True)

