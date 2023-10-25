from urllib.parse import urlencode

from django.conf import settings
from django.utils import timezone
from django.utils.encoding import filepath_to_uri
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import clean_name

AWS_S3_DOMAIN = getattr(settings, "AWS_S3_DOMAIN", None)


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "media/static"
    default_acl = "public-read"

    def url(self, name, parameters=None, expire=None, http_method=None):
        if not AWS_S3_DOMAIN:
            super().url(name, parameters=parameters, expire=expire, http_method=http_method)

        base_url = f"https://{AWS_S3_DOMAIN}/wave-bucket"
        # Preserve the trailing slash after normalizing the path.
        name = self._normalize_name(clean_name(name))
        params = parameters.copy() if parameters else {}
        if expire is None:
            expire = self.querystring_expire

        if self.custom_domain:
            url = "{}/{}{}".format(
                str(base_url).rstrip("/"),
                filepath_to_uri(name),
                f"?{urlencode(params)}" if params else "",
            )

            if self.querystring_auth and self.cloudfront_signer:
                expiration = timezone.datetime.utcnow() + timezone.timedelta(seconds=expire)
                return self.cloudfront_signer.generate_presigned_url(url, date_less_than=expiration)

            return url


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media/media"
    file_overwrite = False
    default_acl = "public-read"

    def url(self, name, parameters=None, expire=None, http_method=None):
        if not AWS_S3_DOMAIN:
            super().url(name, parameters=parameters, expire=expire, http_method=http_method)

        base_url = f"https://{AWS_S3_DOMAIN}/wave-bucket"
        # Preserve the trailing slash after normalizing the path.
        name = self._normalize_name(clean_name(name))
        params = parameters.copy() if parameters else {}
        if expire is None:
            expire = self.querystring_expire

        if self.custom_domain:
            url = "{}/{}{}".format(
                str(base_url).rstrip("/"),
                filepath_to_uri(name),
                f"?{urlencode(params)}" if params else "",
            )

            if self.querystring_auth and self.cloudfront_signer:
                expiration = timezone.datetime.utcnow() + timezone.timedelta(seconds=expire)
                return self.cloudfront_signer.generate_presigned_url(url, date_less_than=expiration)

            return url


location = MediaRootS3Boto3Storage.location
