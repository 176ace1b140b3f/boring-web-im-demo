from flask.ext.testing import TestCase
from web_im.app import create_app
from web_im.exts import db


class BaseTestCase(TestCase):

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/web-im-test.db'

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
