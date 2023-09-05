import pytest
from unittest import mock

import spackle


class TestPricingTable:
    def test_retrieve(self):
        data = {
            "id": "abc123",
            "name": "Test Pricing Table",
            "intervals": ["month", "year"],
            "products": [
                {
                    "id": "prod_abc123",
                    "features": [
                        {
                            "key": "test_feature",
                            "name": "Test Feature",
                            "type": spackle.FEATURE_TYPE_FLAG,
                            "value_flag": True,
                        }
                    ],
                    "name": "Basic",
                    "prices": {
                        "month": {
                            "currency": "usd",
                            "unit_amount": 1000,
                        },
                        "year": {
                            "currency": "usd",
                            "unit_amount": 10000,
                        },
                    },
                }
            ],
        }
        with mock.patch("spackle.pricing_table.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = data
            pricing_table = spackle.PricingTable.retrieve("abc123")

        assert pricing_table == data
