import json
from spackle.stores.base import Store


class FileStore(Store):
    def __init__(self, path):
        self.path = path

    def get_customer_data(self, customer_id):
        with open(self.path, "r") as f:
            data = json.load(f)
        return data.get(customer_id)

    def set_customer_data(self, customer_id, customer_data):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        data[customer_id] = customer_data
        with open(self.path, "w") as f:
            f.write(json.dumps(data))