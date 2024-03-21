import spackle

from unittest import mock

from spackle import ApiStore

spackle.api_key = "abc123"


class TestApiStore:
    def test_retrieve(self):
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "subscriptions": [],
            "features": [{"key": "foo", "value_flag": True, "type": 0}],
        }
        mock_response.status_code = 200

        mock_client = mock.Mock()
        mock_client.get.return_value = mock_response
        with mock.patch("requests.Session", return_value=mock_client):
            spackle.set_store(ApiStore())
            customer = spackle.Customer.retrieve("cus_123")

        assert customer.enabled("foo") is True