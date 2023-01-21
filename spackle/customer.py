import json
import pprint

from spackle import dynamodb, log
from spackle.exceptions import SpackleException

VERSION = 1


class Customer:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @staticmethod
    def retrieve(customer_id):
        log.log_debug("Retrieving customer data for %s" % customer_id)
        dynamodb_client = dynamodb.get_client()
        response = dynamodb_client.get_item(
            {
                "CustomerId": {"S": customer_id},
                "Version": {"N": str(VERSION)}
            }
        )

        data = json.loads(response["Item"]["State"]["S"])
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, data))
        return Customer(customer_id, data)

    @property
    def features(self):
        return self.data["features"]

    @property
    def flag_features(self):
        return [f for f in self.data["features"] if f["type"] == 0]

    @property
    def limit_features(self):
        return [f for f in self.data["features"] if f["type"] == 1]

    def enabled(self, key):
        for feature in self.flag_features:
            if feature["key"] == key:
                return feature["value_flag"]

        raise SpackleException("Flag feature %s not found" % key)

    def limit(self, key):
        for feature in self.limit_features:
            if feature["key"] == key:
                return feature["value_limit"] or float("inf")

        raise SpackleException("Limit feature %s not found" % key)

    def __repr__(self):
        return f"<Customer ({self.id}):\n{pprint.pformat(self.data)}>"
