import pytest

import spackle

from spackle import MemoryStore

spackle.api_key = "abc123"


class TestWaiters:
    def test_wait_for_customer(self):
        spackle.set_store(MemoryStore())

        with pytest.raises(spackle.SpackleException):
            spackle.wait_for_customer("cus_123", timeout=1)

        spackle.get_store().set_customer_data(
            "cus_123",
            {
                "subscriptions": [],
                "features": [{"key": "foo", "value_flag": True, "type": 0}],
            },
        )

        customer = spackle.wait_for_customer("cus_123")
        assert customer.id == "cus_123"

    def test_wait_for_subscription(self):
        spackle.set_store(MemoryStore())

        spackle.get_store().set_customer_data(
            "cus_123",
            {
                "subscriptions": [],
                "features": [{"key": "foo", "value_flag": True, "type": 0}],
            },
        )

        with pytest.raises(spackle.SpackleException):
            spackle.wait_for_subscription("cus_123", "sub_123", timeout=1)

        spackle.get_store().set_customer_data(
            "cus_123",
            {
                "subscriptions": [{"id": "sub_123"}],
                "features": [{"key": "foo", "value_flag": True, "type": 0}],
            },
        )

        sub = spackle.wait_for_subscription("cus_123", "sub_123", timeout=1)
        assert sub.id == "sub_123"

    def test_wait_for_subscription_with_status_filter(self):
        spackle.set_store(MemoryStore())

        spackle.get_store().set_customer_data(
            "cus_123",
            {
                "subscriptions": [{"id": "sub_123", "status": "trialing"}],
                "features": [{"key": "foo", "value_flag": True, "type": 0}],
            },
        )

        with pytest.raises(spackle.SpackleException):
            spackle.wait_for_subscription(
                "cus_123", "sub_123", timeout=1, status="active"
            )

        spackle.get_store().set_customer_data(
            "cus_123",
            {
                "subscriptions": [{"id": "sub_123", "status": "active"}],
                "features": [{"key": "foo", "value_flag": True, "type": 0}],
            },
        )

        sub = spackle.wait_for_subscription(
            "cus_123", "sub_123", timeout=1, status="active"
        )
        assert sub.id == "sub_123"
