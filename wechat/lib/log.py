# -*- coding: UTF-8 -*-
# __author__ = xutao

import logging, logging.config, yaml
from logging.handlers import SMTPHandler


def configure_log(app, path):
    logging.config.dictConfig(yaml.load(open(path)))

    if not app.debug:

        mail_handler = SMTPHandler(
            app.config['MAIL_SERVER'],
            app.config['MAIL_USERNAME'],
            app.config['ADMINS'],
            'Server Error!',
            (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        )

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(mail_handler)
