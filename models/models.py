# -*- coding: utf-8 -*-
"""
    s3-storage.models
    ~~~~~~~~~~~~~~~~~

    Use s3 as file storage mechanism

    :copyright: (c) 2020 by Gabriel Martínez.
    :license: MIT License, see LICENSE for more details.
"""

import hashlib
import base64

from odoo import models
from . import s3_helper


class S3Attachment(models.Model):
    """Extends ir.attachment to implement the S3 storage engine
    """
    _inherit = "ir.attachment"

    def _file_read(self, file_name, bin_size=False):
        s3, bucket_name = s3_helper.get_s3_connection(self)
        if s3 is not None:
            file_exists = s3_helper.s3_object_exists(s3, bucket_name, file_name)
            if file_exists:
                read = base64.b64encode(s3.get_object(Bucket=bucket_name, Key=file_name)['Body'].read())
                return read
        try: # falling back on Odoo's local filestore
            read = super(S3Attachment, self)._file_read(file_name, bin_size=False)
        except Exception:
            return False
        return read

    def _file_write(self, value, checksum):
        s3, bucket_name = s3_helper.get_s3_connection(self)
        if s3 is not None:
            bin_value = base64.b64decode(value)
            file_name = hashlib.sha1(bin_value).hexdigest()
            s3.put_object(Body=bin_value, ContentType=self.mimetype, Key=file_name, Bucket=bucket_name)
        else: # falling back on Odoo's local filestore
            file_name = super(S3Attachment, self)._file_write(value, checksum)
        return file_name


