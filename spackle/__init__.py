import threading
from spackle.customer import Customer
from spackle.exceptions import SpackleException
from spackle.stores import DynamoDBStore, MemoryStore, FileStore
from spackle.constants import FEATURE_TYPE_FLAG, FEATURE_TYPE_LIMIT

api_key = None
api_base = "https://api.spackle.so/v1"
schema_version = 1

_thread = threading.local()


def get_store():
    if not hasattr(_thread, "store"):
        _thread.store = DynamoDBStore()
    return _thread.store


def set_store(store):
    _thread.store = store


def bootstrap():
    get_store()
