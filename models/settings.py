"""
    settings.py
    ~~~~~~~~~~~~~~~~~

    settings model for AWS S3 Bucket

    :copyright: (c) 2020 by Gabriel Martínez.
    :license: MIT License, see LICENSE for more details.
"""

from odoo import models, fields, api


class S3Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    aws_secret_key = fields.Char()
    aws_access_key = fields.Char()
    aws_region = fields.Selection(selection=[('us-east-2','US East (Ohio) - us-east-2'),('us-east-1','US East (N. Virginia) - us-east-1'),('us-west-1','US West (N. California) - us-west-1'),('us-west-2','US West (Oregon) - us-west-2'),('af-south-1','Africa (Cape Town) - af-south-1'),('ap-east-1','Asia Pacific (Hong Kong) - ap-east-1'),('ap-south-1','Asia Pacific (Mumbai) - ap-south-1'),('ap-northeast-3','Asia Pacific (Osaka-Local) - ap-northeast-3'),('ap-northeast-2','Asia Pacific (Seoul) - ap-northeast-2'),('ap-southeast-1','Asia Pacific (Singapore) - ap-southeast-1'),('ap-southeast-2','Asia Pacific (Sydney) - ap-southeast-2'),('ap-northeast-1','Asia Pacific (Tokyo) - ap-northeast-1'),('ca-central-1','Canada (Central) - ca-central-1'),('cn-north-1','China (Beijing) - cn-north-1'),('cn-northwest-1','China (Ningxia) - cn-northwest-1'),('eu-central-1','Europe (Frankfurt) - eu-central-1'),('eu-west-1','Europe (Ireland) - eu-west-1'),('eu-west-2','Europe (London) - eu-west-2'),('eu-south-1','Europe (Milan) - eu-south-1'),('eu-west-3','Europe (Paris) - eu-west-3'),('eu-north-1','Europe (Stockholm) - eu-north-1'),('me-south-1','Middle East (Bahrain) - me-south-1'),('sa-east-1','South America (São Paulo) - sa-east-1')])
    aws_bucket_name = fields.Char()
    aws_s3_storage_enable = fields.Boolean()

    def set_values(self):
        res = super(S3Settings, self).set_values()
        self.env['ir.config_parameter'].set_param('aws_secret_key', self.aws_secret_key)
        self.env['ir.config_parameter'].set_param('aws_access_key', self.aws_access_key)
        self.env['ir.config_parameter'].set_param('aws_region', self.aws_region)
        self.env['ir.config_parameter'].set_param('aws_bucket_name', self.aws_bucket_name)
        self.env['ir.config_parameter'].set_param('aws_s3_storage_enable', self.aws_s3_storage_enable)
        return res

    @api.model
    def get_values(self):
        res = super(S3Settings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        aws_secret_key = icp_sudo.get_param('aws_secret_key')
        aws_access_key = icp_sudo.get_param('aws_access_key')
        aws_region = icp_sudo.get_param('aws_region')
        aws_bucket_name = icp_sudo.get_param('aws_bucket_name')
        aws_s3_storage_enable = icp_sudo.get_param('aws_s3_storage_enable')
        res.update(
            aws_secret_key = aws_secret_key,
            aws_access_key = aws_access_key,
            aws_region = aws_region,
            aws_bucket_name = aws_bucket_name,
            aws_s3_storage_enable = aws_s3_storage_enable
        )
        return res
