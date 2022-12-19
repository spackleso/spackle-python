import spackle

spackle.api_key = "abc123"


class TestCustomer:
    def test_retrieve(self, requests_mock):
        requests_mock.post(
            "https://api.spackle.so/auth/session",
            json={},
        )
        spackle.Customer.retrieve("cus_123")
        assert requests_mock.call_count == 1
        req = requests_mock.last_request
        assert req.headers["Authorization"] == "Bearer abc123"

    def test_enabled(self):
        customer = spackle.Customer(
            data={
                "subscriptions": [],
                "features": [{"key": "foo", "value_flag": True}],
            }
        )
        assert customer.enabled("foo") is True
        assert customer.enabled("bar") is False

    def test_limit(self):
        customer = spackle.Customer(
            data={
                "subscriptions": [],
                "features": [{"key": "foo", "value_limit": 100}],
            }
        )
        assert customer.limit("foo") == 100
        assert customer.limit("bar") == 0
