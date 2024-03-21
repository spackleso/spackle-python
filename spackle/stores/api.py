import json
import requests
import threading

from spackle import log
from spackle.exceptions import SpackleException


class ApiStore:
    _thread_local = None

    def __init__(self):
        self._thread_local = threading.local()

    def get_customer_data(self, customer_id):
        from spackle import api_base, api_key, schema_version

        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = requests.Session()

        response = self._thread_local.session.get(
            f"{api_base}/customers/{customer_id}/state",
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-Spackle-Schema-Version": str(schema_version),
            },
        )

        if response.status_code != 200:
            raise SpackleException(
                "Customer %s not found; status code: %s; response: %s"
                % (customer_id, response.status_code, response.text)
            )

        data = response.json()
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, data))
        return data