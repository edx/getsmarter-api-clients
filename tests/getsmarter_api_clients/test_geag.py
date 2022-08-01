"""
Tests for the GEAG client.
"""

import json
from datetime import datetime
from unittest import mock

import ddt
import pytz
import responses

from getsmarter_api_clients.geag import GetSmarterEnterpriseApiClient
from tests.getsmarter_api_clients.test_oauth import BaseOAuthApiClientTests


@ddt.ddt
class GetSmarterEnterpriseApiClientTests(BaseOAuthApiClientTests):
    """
    Tests for GetSmarterEnterpriseApiClient.
    """
    def setUp(self):
        super().setUp()

        self.tiered_cache_patcher = mock.patch('getsmarter_api_clients.oauth.TieredCache')
        self.mock_tiered_cache = self.tiered_cache_patcher.start()
        self.mock_tiered_cache.get_cached_response.return_value = mock.MagicMock(
            value={
                'access_token': 'bcde',
                'expires_in': 60,
                'expires_at': datetime.now(pytz.utc).timestamp() + 60
            },
            is_found=True
        )

        self.addCleanup(self.tiered_cache_patcher.stop)

    @responses.activate
    def test_get_terms_and_policies(self):
        terms_and_conditions = {
            'privacyPolicy': 'abcd',
            'websiteTermsOfUse': 'efgh',
        }

        responses.add(
            responses.GET,
            f'{self.api_url}/terms',
            body=json.dumps(terms_and_conditions),
            status=200,
        )

        client = GetSmarterEnterpriseApiClient(**self.mock_constructor_args)
        response = client.get_terms_and_policies()
        self.assertEqual(response, terms_and_conditions)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, f'{self.api_url}/terms')
