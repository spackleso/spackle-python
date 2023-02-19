class Subscription:
    def __init__(self, data):
        self.id = data["id"]
        self.status = data["status"]
        self.price = data["price"]
        self.product = data["product"]
