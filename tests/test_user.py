from flask.ext.testing import TestCase
import pytest
import sqlalchemy.exc
from web_im.exts import db
from web_im.app import create_app
from web_im.models.user import User


class UserTestCase(TestCase):

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/web-im-test.db'

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        uid1 = User.create("jack", "password")
        assert uid1 is not None
        with pytest.raises(sqlalchemy.exc.IntegrityError) as excinfo:
            User.create("jack", "password")

        uid2 = User.create("tom", "password2")
        assert uid2 is not None

    def test_retrieval(self):
        uid1 = User.create("jack", "password")
        user = User.get(uid1)
        user2 = User.get_by_name("jack")
        assert user.id == user2.id

        assert None is User.get(999)
        assert None is User.get_by_name("not-existed")

    def test_login_challenge(self):
        uid = User.create("jack", "password")
        assert uid is not None
        assert uid == User.login_challenge("jack", "password")
        assert None is User.login_challenge("jack2", "password")
        assert None is User.login_challenge("jack2", "password2")
