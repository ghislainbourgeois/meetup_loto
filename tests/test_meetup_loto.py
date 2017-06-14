import tests.context
import unittest

from tests.api_mock import FakeApi
from meetup_loto import Loto

class TestMeetupLoto(unittest.TestCase):
    def setUp(self):
        self.api = FakeApi()
        self.loto = Loto(self.api, "Docker-Montreal", 240672864)

    def test_meetup_loto_participants(self):
        nb_participants = self.loto.number_of_participants()
        self.assertEquals(10, nb_participants)
        self.assertEquals(0.1, self.loto.current_chances())

    def test_meetup_loto_winner(self):
        winner = self.loto.draw()
        self.assertTrue(winner >= 1 and winner <= 10)

    def test_meetup_loto_multiple_draw(self):
        winners = []
        for i in range(11):
            winner = self.loto.draw()
            self.assertFalse(winner in winners)
            winners.append(winner)
        self.assertEquals(0, winners[-1])


