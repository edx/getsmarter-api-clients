"""
Tests for the OAuth client.
"""

import json
from datetime import datetime
from unittest import TestCase, mock

import ddt
import pytz
import responses

from getsmarter_api_clients.oauth import OAuthApiClient


class BaseOAuthApiClientTests(TestCase):
    """
    Base class for client tests.
    """
    def setUp(self):
        super().setUp()

        self.client_id = 'client-id'
        self.client_secret = 'client-secret'
        self.provider_url = 'https://provider-url.com'
        self.api_url = 'https://api-url.com'

        self.mock_constructor_args = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'provider_url': self.provider_url,
            'api_url': self.api_url
        }


@ddt.ddt
class OAuthApiClientTests(BaseOAuthApiClientTests):
    """
    Tests for OAuthApiClient.
    """
    def mock_access_token(
        self,
        token='abcd',
    ):
        responses.add(
            responses.POST,
            f'{self.provider_url}/oauth2/token',
            body=json.dumps({
                'access_token': token,
                'expires_in': 300,
                'expires_at': datetime.now(pytz.utc).timestamp() + 300
            }),
            status=200,
        )

    @mock.patch('getsmarter_api_clients.oauth.TieredCache')
    @responses.activate
    def test_get_access_token(self, mock_tiered_cache):
        """
        Test that client can get an access token using the client credentials.
        """
        mock_tiered_cache.get_cached_response.return_value = mock.MagicMock(is_found=False)
        self.mock_access_token('abcd')
        client = OAuthApiClient(**self.mock_constructor_args)
        access_token = client._get_access_token()   # pylint: disable=protected-access

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, f'{self.provider_url}/oauth2/token')
        self.assertEqual(access_token, 'abcd')

    @ddt.data(
        (False, 'bcde'),
        (True, 'abcd'),
    )
    @ddt.unpack
    @mock.patch('getsmarter_api_clients.oauth.TieredCache')
    @responses.activate
    def test_cached_access_token(self, is_expired, expected_token, mock_tiered_cache):
        """
        Test that the cached token is used if it's not expired.
        """

        mock_tiered_cache.get_cached_response.return_value = mock.MagicMock(
            value={
                'access_token': 'bcde',
                'expires_in': 60,
                'expires_at': datetime.now(pytz.utc).timestamp() + (-60 if is_expired else 60)
            },
            is_found=True
        )

        self.mock_access_token('abcd')
        client = OAuthApiClient(**self.mock_constructor_args)
        access_token = client._get_access_token()   # pylint: disable=protected-access

        self.assertEqual(len(responses.calls), 1 if is_expired else 0)
        self.assertEqual(access_token, expected_token)
