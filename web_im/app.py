# coding: utf-8

import logging
from werkzeug.utils import import_string
from flask import Flask, url_for

from web_im.exts import db

logger = logging.getLogger(__name__)
blueprints = [
    "home",
    "api.user",
    "api.chat",
]


def create_app(config=None):
    app = Flask(__name__)

    config_app(app, config)
    config_blueprints(app)
    config_extensions(app)
    config_templates(app)
    return app


def config_app(app, config=None):
    """TODO: override on prod
    """
    app.config.from_object('web_im.config.DevelopmentConfig')

    if config:
        app.config.from_object(config)


def config_blueprints(app):
    for bp in blueprints:
        app.register_blueprint(
            import_string("%s.views.%s:bp" % (__package__, bp))
        )


def config_extensions(app):
    db.init_app(app)


def config_templates(app):
    app.jinja_env.globals['static_url_for'] = lambda filename: url_for(
        "static", filename=filename
    )


__all__ = ["create_app"]
