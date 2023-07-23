import spackle

from unittest import mock

from spackle import EdgeStore

spackle.api_key = "abc123"


class TestEdgeStore:
    def test_retrieve(self):
        mock_client = mock.Mock()
        mock_response = mock.Mock()
        mock_response.data = b'{"subscriptions": [], "features": [{"key": "foo", "value_flag": true, "type": 0}]}'
        mock_response.status = 200
        mock_client.request.return_value = mock_response

        with mock.patch("urllib3.PoolManager", return_value=mock_client):
            spackle.set_store(EdgeStore())

        customer = spackle.Customer.retrieve("cus_123")
        assert customer.enabled("foo") is True
