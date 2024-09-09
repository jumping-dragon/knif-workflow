import logging
import os

LOGGER_LEVEL = int(os.environ.get("LOGGER_LEVEL", logging.INFO))

CONN_STR = os.environ["CONN_STR"]
SCHEMA = os.environ["SCHEMA"]

S3_URL = os.environ["S3_URL"]
S3_USER = os.environ["S3_USER"]
S3_PASS = os.environ["S3_PASS"]

KNATIVE_BROKER_URL = os.environ["KNATIVE_BROKER_URL"]
