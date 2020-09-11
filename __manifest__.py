# -*- coding: utf-8 -*-
{
    'name': "Odoo AWS S3 Storage",

    'summary': """
        Allows to use Amazon S3 Bucket as file storage""",

    'description': """
        Binary files such as attachments and pictures are stored by default
        in the file system of the host running Odoo. In some cases you may
        want to decrease the overall response time by delegating static file
        storage to a specialized instance such as an DigitalOcean Spaces bucket.
        This module allows you to configure Odoo so that an DigitalOcean Spaces bucket is
        used instead of the file system for binary files storage.
    """,

    'author': "gabrielmartinez, marstom",
    'website': "https://marstom.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Technical Settings',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'data' : [
        'views/settings.xml'
    ]
}
