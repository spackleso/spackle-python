import os
import spackle
from flask import Flask

spackle.api_key = os.getenv("SPACKLE_API_KEY")
spackle.log = "debug"
spackle.bootstrap()


app = Flask(__name__)


@app.route("/")
def hello_world():
    customer_id = os.getenv("SPACKLE_CUSTOMER_ID")
    if not customer_id:
        return "<p>SPACKLE_CUSTOMER_ID not set</p>"

    feature_key = os.getenv("SPACKLE_FEATURE_KEY")
    if not feature_key:
        return "<p>SPACKLE_FEATURE_KEY not set</p>"

    spackle_customer = spackle.Customer.retrieve(customer_id)
    return f"<p>{spackle_customer.enabled(feature_key)}</p>"
