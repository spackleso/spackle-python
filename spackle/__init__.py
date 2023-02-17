import threading
from spackle.customer import Customer
from spackle.exceptions import SpackleException
from spackle.stores import DynamoDBStore

api_key = None
api_base = "https://api.spackle.so/v1"
store_cls = DynamoDBStore
schema_version = 1


_thread = threading.local()


def get_store():
    if not hasattr(_thread, "adapter") or not isinstance(_thread.adapter, store_cls):
        _thread.adapter = store_cls()
    return _thread.adapter


def bootstrap():
    get_store()
