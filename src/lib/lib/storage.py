import io
from functools import cached_property
from typing import Any

from minio import Minio

from .config import S3_PASS, S3_URL, S3_USER
from .log import logger


class MinioWrapper(Minio):
    def __init__(
        self, endpoint: str, access_key: str, secret_key: str, bucket_name: str
    ):
        self.minio = Minio(
            endpoint, access_key=access_key, secret_key=secret_key, secure=False
        )
        self.ensure_bucket(bucket_name)

    @cached_property
    def bucket_name(self) -> str:
        return self._bucket_name

    def ensure_bucket(self, bucket_name: str):
        # Make the bucket if it doesn't exist.
        bucket_exist = self.minio.bucket_exists(bucket_name)
        if not bucket_exist:
            self.minio.make_bucket(bucket_name)
        self._bucket_name = bucket_name

    def get_object(self, key: str):
        try:
            response = self.minio.get_object(self.bucket_name, key)
        except Exception as err:
            logger.error(f"ERR get_content {err}")
        finally:
            yield response
            response.close()
            response.release_conn()

    def put_object(self, key: str, data: bytes, **kwargs: Any):
        try:
            return self.minio.put_object(
                bucket_name=self.bucket_name,
                data=io.BytesIO(data),
                object_name=key,
                length=len(data),
                **kwargs,
            )
        except Exception as err:
            logger.error(f"ERR put_content {err}")


CISA_BUCKET = MinioWrapper(
    S3_URL, access_key=S3_USER, secret_key=S3_PASS, bucket_name="cisa"
)

ESET_BUCKET = MinioWrapper(
    S3_URL, access_key=S3_USER, secret_key=S3_PASS, bucket_name="eset"
)

JPCERT_BUCKET = MinioWrapper(
    S3_URL, access_key=S3_USER, secret_key=S3_PASS, bucket_name="jpcert"
)

MANDIANT_BUCKET = MinioWrapper(
    S3_URL, access_key=S3_USER, secret_key=S3_PASS, bucket_name="mandiant"
)

SYMANTEC_BUCKET = MinioWrapper(
    S3_URL, access_key=S3_USER, secret_key=S3_PASS, bucket_name="symantec"
)

UNIT42_BUCKET = MinioWrapper(
    S3_URL, access_key=S3_USER, secret_key=S3_PASS, bucket_name="unit42"
)
