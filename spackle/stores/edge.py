import json
import urllib3

from spackle import log
from spackle.exceptions import SpackleException


class EdgeStore:
    def __init__(self):
        self.http = urllib3.PoolManager()

    def get_customer_data(self, customer_id):
        from spackle import api_key, edge_base, schema_version

        response = self.http.request(
            "GET",
            f"{edge_base}/customers/{customer_id}/state",
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-Spackle-Schema-Version": schema_version,
            },
        )

        if response.status != 200:
            return self._fetch_state_from_api(customer_id)

        body = response.data.decode("utf-8")
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, body))
        return json.loads(body)

    def _fetch_state_from_api(self, customer_id):
        from spackle import api_key, api_base

        log.log_warn("Customer %s not found in store, using API" % customer_id)
        response = self.http.request(
            "GET",
            f"{api_base}/customers/{customer_id}/state",
            headers={"Authorization": f"Bearer {api_key}"},
        )

        if response.status_code != 200:
            raise SpackleException(
                "Customer %s not found; status code: %s; response: %s"
                % (customer_id, response.status, response.data.decode("utf-8"))
            )

        body = response.data.decode("utf-8")
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, body))
        return json.loads(body)
