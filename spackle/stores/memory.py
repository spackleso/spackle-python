from spackle import SpackleException
from spackle.stores.base import Store


class MemoryStore(Store):
    def __init__(self):
        self.data = {}

    def get_customer_data(self, customer_id):
        try:
            return self.data[customer_id]
        except KeyError:
            raise SpackleException("Customer %s not found" % customer_id)

    def set_customer_data(self, customer_id, data):
        self.data[customer_id] = data
