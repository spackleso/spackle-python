from spackle.stores.base import Store


class MemoryStore(Store):
    def __init__(self):
        self.data = {}

    def get_customer_data(self, customer_id):
        return self.data.get(customer_id, {
            "features": [],
            "subscriptions": [],
        })

    def set_customer_data(self, customer_id, data):
        self.data[customer_id] = data
