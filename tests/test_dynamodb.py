import spackle

from unittest import mock

from spackle import DynamoDBStore

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

        with mock.patch(
            "spackle.stores.dynamodb.DynamoDBStore._bootstrap_client",
            return_value=mock_client,
        ):
            spackle.set_store(DynamoDBStore())

        customer = spackle.Customer.retrieve("cus_123")
        assert customer.enabled("foo") is True
