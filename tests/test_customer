import pytest

import spackle


class TestCustomer:
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
