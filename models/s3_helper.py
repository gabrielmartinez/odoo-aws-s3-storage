"""
    s3_helper.py
    ~~~~~~~~~~~~~~~~~

    Helper functions for models.py

    :copyright: (c) 2020 by Gabriel Martínez.
    :license: MIT License, see LICENSE for more details.
"""

import boto3
# uncomment for debug mode:
# boto3.set_stream_logger('')
import botocore
from boto3.session import Session
from boto3.s3.transfer import S3Transfer
from botocore.exceptions import ClientError


def s3_bucket_exists(s3, bucket_name):
    exists = True
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False
    return exists


def s3_object_exists(s3, bucket_name, key):
    exists = True
    try:
        s3.head_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False
    return exists


def get_s3_connection(parent):
    # Getting Values
    s3 = None
    icp_sudo = parent.env['ir.config_parameter'].sudo()
    aws_secret_key = icp_sudo.get_param('aws_secret_key')
    aws_access_key = icp_sudo.get_param('aws_access_key')
    aws_region = icp_sudo.get_param('aws_region')
    aws_bucket_name = icp_sudo.get_param('aws_bucket_name')
    enable = icp_sudo.get_param('aws_s3_storage_enable')
    aws_s3_storage_enable = (enable == 'True')
    if aws_s3_storage_enable :
        session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
        s3 = session.client('s3')
        if not s3_bucket_exists(s3, aws_bucket_name):
            s3 = None
    return s3, aws_bucket_name


# def parse_bucket_url(bucket_url):
#     scheme = bucket_url[:5]
#     assert scheme == 's3://', \
#         "Expecting an s3:// scheme, got {} instead.".format(scheme)
#
#     # scheme:
#     # s3://<Your-AWS-Access-Key-ID>:<Your-AWS-Secret-Key>@<Your-S3-Bucket-name>&<Your-DigitalOcean-base-url>+SSE
#     # where +SSE is optional (meaning server-side encryption enabled)
#
#     try:
#         encryption_enabled = False
#         remain = bucket_url.lstrip(scheme)
#         access_key_id = remain.split(':')[0]
#         remain = remain.lstrip(access_key_id).lstrip(':')
#         secret_key = remain.split('@')[0]
#         remain = remain.lstrip(secret_key).lstrip('@')
#         bucket_name = remain.split('&')[0]
#         remain = remain.lstrip(bucket_name).lstrip('&').split('+')
#         do_space_url = remain[0]
#         encryption_enabled = len(remain) > 1
#
#         if not access_key_id or not secret_key:
#             raise Exception(
#                 "No AWS access and secret keys were provided."
#                 " Unable to establish a connexion to S3."
#             )
#     except Exception:
#         raise Exception("Unable to parse the S3 bucket url.")
#
#     return (access_key_id, secret_key, bucket_name, do_space_url, encryption_enabled)
#
#
# def bucket_exists(s3, bucket_name):
#     exists = True
#     try:
#         s3.meta.client.head_bucket(Bucket=bucket_name)
#     except botocore.exceptions.ClientError as e:
#         error_code = int(e.response['Error']['Code'])
#         if error_code == 404:
#             exists = False
#     return exists
#
#
# def object_exists(s3, bucket_name, key):
#     exists = True
#     try:
#         s3.meta.client.head_object(Bucket=bucket_name, Key=key)
#     except botocore.exceptions.ClientError as e:
#         error_code = int(e.response['Error']['Code'])
#         if error_code == 404:
#             exists = False
#     return exists
#
#
# def get_resource(access_key_id, secret_key, endpoint_url):
#     session = boto3.Session(access_key_id, secret_key)
#     s3 = session.resource('s3', endpoint_url='https://' + endpoint_url)
#     return s3
#
#
# # extra: works for files stored in the file system
# # (not called by models.py which only deal with in-memory)
# def upload(value, storage):
#     access_key_id, secret_key, bucket_name, do_space_url, encryption_enabled = parse_bucket_url(storage)
#     s3 = get_resource(access_key_id, secret_key)
#     ### S3Transfer allows multi-part, call backs etc
#     # http://boto3.readthedocs.io/en/latest/_modules/boto3/s3/transfer.html
#     transfer = S3Transfer(s3.meta.client)
#     if encryption_enabled:
#         transfer.upload_file(value, bucket_name, do_space_url, value, extra_args={'ServerSideEncryption': 'AES256'})
#     else:
#         transfer.upload_file(value, bucket_name, do_space_url, value)
