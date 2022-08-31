"""
Tests for the GEAG client.
"""

import ast
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
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.terms_url = f'{self.api_url}/terms'
        self.allocations_url = f'{self.api_url}/allocations'

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
            self.terms_url,
            body=json.dumps(terms_and_conditions),
            status=200,
        )

        client = GetSmarterEnterpriseApiClient(**self.mock_constructor_args)
        response = client.get_terms_and_policies()
        self.assertEqual(response, terms_and_conditions)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, self.terms_url)

    @responses.activate
    def test_create_allocation(self):
        responses.add(
            responses.POST,
            self.allocations_url,
            status=204,
        )
        client = GetSmarterEnterpriseApiClient(**self.mock_constructor_args)

        kwargs = {
            'payment_reference': 'payment_reference',
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'johnsmith@example.com',
            'date_of_birth': '2000-01-01',
            'terms_accepted_at': '2022-07-25T10:29:56Z',
            'currency': 'USD',
            'order_items': [
                {
                    # productId will be the variant id from product details
                    'productId': '87c24e19-b82c-4acd-ab90-714af629f11a',
                    'quantity': 1,
                    'normalPrice': 1000,
                    'discount': 1000,
                    'finalPrice': 0
                }
            ],
            'address_line1': '10 Lovely Street',
            'city': 'Herndon',
            'postal_code': '35005',
            'state': 'Alabama',
            'state_code': 'state_code',
            'country': 'country',
            'country_code': 'country_code',
            'mobile_phone': '+12015551234',
            'work_experience': 'None',
            'enterprise_customer_uuid': '731b28ee-09d1-4b89-8f7b-2c8fd0939746'
        }
        client.create_allocation(**kwargs)

        expected_payload = {
            'paymentReference': kwargs['payment_reference'],
            'firstName': kwargs['first_name'],
            'lastName': kwargs['last_name'],
            'email': kwargs['email'],
            'dateOfBirth': kwargs['date_of_birth'],
            'termsAcceptedAt': kwargs['terms_accepted_at'],
            'currency': kwargs['currency'],
            'orderItems': kwargs['order_items'],
            'addressLine1': kwargs['address_line1'],
            'city': kwargs['city'],
            'postalCode': kwargs['postal_code'],
            'state': kwargs['state'],
            'stateCode': kwargs['state_code'],
            'country': kwargs['country'],
            'countryCode': kwargs['country_code'],
            'mobilePhone': kwargs['mobile_phone'],
            'workExperience': kwargs['work_experience'],
            'enterprise_customer_uuid': kwargs['enterprise_customer_uuid']
        }

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, self.allocations_url)
        self.assertDictEqual(ast.literal_eval(responses.calls[0].request.body.decode('utf-8')), expected_payload)
