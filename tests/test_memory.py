import spackle

import pytest
from unittest import mock
from spackle.stores.memory import MemoryStore

spackle.api_key = "abc123"


class TestCustomer:
    def test_retrieve(self):
        spackle.store_cls = MemoryStore
        spackle.get_store().set_customer_data(
            "cus_123",
            {
                "subscriptions": [],
                "features": [{"key": "foo", "value_flag": True, "type": 0}],
            },
        )
        customer = spackle.Customer.retrieve("cus_123")
        assert customer.enabled("foo") is True