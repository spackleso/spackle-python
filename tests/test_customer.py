import spackle

import pytest
from unittest import mock

spackle.api_key = "abc123"


class TestCustomer:
    def test_retrieve(self):
        mock_client = mock.Mock()
        mock_client.query.return_value = {
            "Items": [
                {
                    "State": {
                        "S": '{"subscriptions": [], "features": [{"key": "foo", "value_flag": true, "type": 0}]}'
                    }
                }
            ]
        }

        with mock.patch("spackle.dynamodb.get_client", return_value=mock_client):
            customer = spackle.Customer.retrieve("cus_123")

        assert customer.enabled("foo") is True

    def test_enabled(self):
        customer = spackle.Customer(
            "cus_123",
            data={
                "subscriptions": [],
                "features": [{"key": "foo", "value_flag": True, "type": 0}],
            },
        )
        assert customer.enabled("foo") is True
        with pytest.raises(spackle.SpackleException):
            customer.enabled("bar")

    def test_limit(self):
        customer = spackle.Customer(
            "cus_123",
            data={
                "subscriptions": [],
                "features": [
                    {"key": "foo", "value_limit": 100, "type": 1},
                    {"key": "unlimited", "value_limit": None, "type": 1},
                    {"key": "zero", "value_limit": 0, "type": 1},
                ],
            },
        )
        assert customer.limit("foo") == 100
        assert customer.limit("unlimited") == float("inf")
        assert customer.limit("unlimited") > 100
        assert customer.limit("zero") == 0
        with pytest.raises(spackle.SpackleException):
            customer.limit("bar")
