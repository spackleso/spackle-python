from functools import lru_cache
import boto3
import requests
from spackle import log
from botocore.credentials import RefreshableCredentials
from boto3 import Session
from botocore.session import get_session


class DynamoDB:
    client = None
    identity_id = None
    table_name = None
    aws_region = None

    def __init__(self):
        self.client = self._bootstrap_client()

    def _bootstrap_client(self):
        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self._fetch_credentials(),
            refresh_using=self._fetch_credentials,
            method="sts-assume-role-with-web-identity",
        )
        session = get_session()
        session._credentials = session_credentials
        session.set_config_variable("region", self.aws_region)
        autorefresh_session = Session(botocore_session=session)
        return autorefresh_session.client("dynamodb", region_name=self.aws_region)

    def _fetch_credentials(self):
        from spackle import api_key, api_base

        log.log_debug("Bootstrapping DynamoDB client...")
        session = requests.post(
            f"{api_base}/auth/session",
            headers={"Authorization": f"Bearer {api_key}"},
        ).json()
        self.identity_id = session["identity_id"]
        self.table_name = session["table_name"]
        self.aws_region = session["aws_region"]
        log.log_debug("Created session: %s" % session)

        sts_client = boto3.client("sts")
        response = sts_client.assume_role_with_web_identity(
            RoleArn=session["role_arn"],
            RoleSessionName=session["account_id"],
            WebIdentityToken=session["token"],
        )
        return {
            "access_key": response["Credentials"]["AccessKeyId"],
            "secret_key": response["Credentials"]["SecretAccessKey"],
            "token": response["Credentials"]["SessionToken"],
            "expiry_time": response["Credentials"]["Expiration"].isoformat(),
        }


@lru_cache(maxsize=1)
def get_client():
    log.log_debug("Creating DynamoDB client...")
    return DynamoDB()
