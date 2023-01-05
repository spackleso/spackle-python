import spackle

from unittest import mock

spackle.api_key = "abc123"


class TestCustomer:
    def test_retrieve(self):
        mock_client = mock.Mock()
        mock_client.client.get_item.return_value = {
            "Item": {
                "State": {
                    "S": '{"subscriptions": [], "features": [{"key": "foo", "value_flag": true}]}'
                }
            }
        }

        with mock.patch("spackle.dynamodb.get_client", return_value=mock_client):
            customer = spackle.Customer.retrieve("cus_123")

        assert customer.enabled("foo") is True

    def test_enabled(self):
        customer = spackle.Customer(
            "cus_123",
            data={
                "subscriptions": [],
                "features": [{"key": "foo", "value_flag": True}],
            },
        )
        assert customer.enabled("foo") is True
        assert customer.enabled("bar") is False

    def test_limit(self):
        customer = spackle.Customer(
            "cus_123",
            data={
                "subscriptions": [],
                "features": [{"key": "foo", "value_limit": 100}],
            },
        )
        assert customer.limit("foo") == 100
        assert customer.limit("bar") == 0
