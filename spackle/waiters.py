import time

from spackle.customer import Customer
from spackle.exceptions import SpackleException


def wait_for_customer(customer_id, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            return Customer.retrieve(customer_id)
        except SpackleException:
            time.sleep(1)

    raise SpackleException("Timed out waiting for customer")


def wait_for_subscription(customer_id, subscription_id, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            customer = Customer.retrieve(customer_id)
            return next(
                sub for sub in customer.subscriptions if sub["id"] == subscription_id
            )
        except (SpackleException, StopIteration):
            time.sleep(1)

    raise SpackleException("Timed out waiting for subscription")
