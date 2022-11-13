import spackle

spackle.api_key = "abc123"


class TestCustomer:
    def test_retrieve(self, requests_mock):
        requests_mock.get(
            "https://www.spackle.so/api/v1/customers/cus_123/state",
            json={
                "subscriptions": [],
                "features": [],
            },
        )
        spackle.Customer.retrieve("cus_123")
        assert requests_mock.call_count == 1
        req = requests_mock.last_request
        assert req.headers["Authorization"] == "Bearer abc123"

    def test_enabled(self):
        customer = spackle.Customer(
            data={
                "subscriptions": [],
                "features": [{"name": "foo", "value_enabled": True}],
            }
        )
        assert customer.enabled("foo") is True
        assert customer.enabled("bar") is False

    def test_limit(self):
        customer = spackle.Customer(
            data={
                "subscriptions": [],
                "features": [{"name": "foo", "value_limit": 100}],
            }
        )
        assert customer.limit("foo") == 100
        assert customer.limit("bar") == 0
