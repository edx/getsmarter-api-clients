"""
Tests for the GEAG client.
"""

from unittest import TestCase

from get_smarter_api_clients.geag import stub


class StubTests(TestCase):
    def test_stub(self):
        stub()
