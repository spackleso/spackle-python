import json

from spackle import SpackleException
from spackle.stores.base import Store


class FileStore(Store):
    def __init__(self, path):
        self.path = path

    def get_customer_data(self, customer_id):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        try:
            return data[customer_id]
        except KeyError:
            raise SpackleException("Customer %s not found" % customer_id)

    def set_customer_data(self, customer_id, customer_data):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        data[customer_id] = customer_data
        with open(self.path, "w") as f:
            f.write(json.dumps(data))
