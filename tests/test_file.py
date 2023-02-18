import json
import pytest
from unittest import mock

import spackle
from spackle import FileStore

spackle.api_key = "abc123"


class TestCustomer:
    def test_retrieve(self):
        path = '/tmp/spackle.json'
        spackle.set_store(FileStore(path))
        spackle.get_store().set_customer_data(
            "cus_123",
            {
                "subscriptions": [],
                "features": [{"key": "foo", "value_flag": True, "type": 0}],
            },
        )
        customer = spackle.Customer.retrieve("cus_123")
        assert customer.enabled("foo") is True

        with open(path, "r") as f:
            data = json.load(f)
            assert data == {
                "cus_123": {
                    "subscriptions": [],
                    "features": [{"key": "foo", "value_flag": True, "type": 0}],
                }
            }
