import spackle

from unittest import mock

from spackle import EdgeStore

spackle.api_key = "abc123"


class TestEdgeStore:
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
            spackle.set_store(EdgeStore())
            customer = spackle.Customer.retrieve("cus_123")

        assert customer.enabled("foo") is True

    def test_retrieve_fallback_to_api(self):
        mock_error_response = mock.Mock()
        mock_error_response.status_code = 404
        mock_error_response.text.return_value = ""

        mock_error_client = mock.Mock()
        mock_error_client.get.return_value = mock_error_response

        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "subscriptions": [],
            "features": [{"key": "foo", "value_flag": True, "type": 0}],
        }
        mock_response.status_code = 200

        with mock.patch("requests.Session", return_value=mock_error_client):
            with mock.patch("requests.get", return_value=mock_response):
                spackle.set_store(EdgeStore())
                customer = spackle.Customer.retrieve("cus_123")

        assert customer.enabled("foo") is True
