import boto3
import requests
import threading
from datetime import datetime, timezone
from spackle import log

config = threading.local()


def get_client():
    if not hasattr(config, "client"):
        log.log_debug("Client not found, bootstrapping...")
        _bootstrap_client()
    elif not hasattr(config, "aws_access_key_id"):
        log.log_debug("AWS Access Key ID not found, bootstrapping...")
        _bootstrap_client()
    elif not hasattr(config, "aws_secret_access_key"):
        log.log_debug("AWS Secret Access Key not found, bootstrapping...")
        _bootstrap_client()
    elif not hasattr(config, "aws_session_token"):
        log.log_debug("AWS Session Token not found, bootstrapping...")
        _bootstrap_client()
    elif not hasattr(config, "aws_region"):
        log.log_debug("AWS Region not found, bootstrapping...")
        _bootstrap_client()
    elif not hasattr(config, "aws_session_expiration"):
        log.log_debug("AWS Session Expiration not found, bootstrapping...")
        _bootstrap_client()
    elif config.aws_session_expiration < datetime.now(timezone.utc):
        log.log_debug("AWS Session Expiration has expired, bootstrapping...")
        _bootstrap_client()

    return config.client


def _bootstrap_client():
    log.log_debug("Bootstrapping DynamoDB client...")
    from spackle import api_key, api_base

    session = requests.post(
        f"{api_base}/auth/session",
        headers={"Authorization": f"Bearer {api_key}"},
    ).json()
    log.log_debug("Created session: %s" % session)

    sts_client = boto3.client("sts")
    credentials = sts_client.assume_role_with_web_identity(
        RoleArn=session["role_arn"],
        RoleSessionName=session["account_id"],
        WebIdentityToken=session["token"],
    )

    config.identity_id = session["identity_id"]
    config.table_name = session["table_name"]
    config.aws_access_key_id = credentials["Credentials"]["AccessKeyId"]
    config.aws_region = session["aws_region"]
    config.aws_secret_access_key = credentials["Credentials"]["SecretAccessKey"]
    config.aws_session_token = credentials["Credentials"]["SessionToken"]
    config.aws_session_expiration = credentials["Credentials"]["Expiration"]

    config.client = boto3.client(
        "dynamodb",
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
        region_name=config.aws_region,
    )
