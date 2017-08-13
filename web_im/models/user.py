import os
import hashlib
import sqlalchemy.orm.exc
from web_im.exts import db


class User(db.Model):
    """
    sha256_password = sha256(raw_password + salt)
    TODO: validate username
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, index=True)
    salt = db.Column(db.String(16))
    sha256_password = db.Column(db.String(32))

    @classmethod
    def create(cls, name, raw_password):
        user = cls()
        user.name = name
        user.salt = os.urandom(16)
        hsh = hashlib.sha256()
        hsh.update(bytes(raw_password, "utf-8") + user.salt)
        user.sha256_password = hsh.digest()
        db.session.add(user)
        try:
            db.session.commit()
            db.session.flush()
            return user.id
        except BaseException as exc:
            db.session.rollback()
            raise exc

    @classmethod
    def get(cls, id_):
        return db.session.query(cls).get(id_)

    @classmethod
    def get_by_name(cls, name):
        try:
            return db.session.query(cls). \
                filter(cls.name == name).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    @classmethod
    def login_challenge(cls, username, raw_password):
        """return user id or None
        """
        user = cls.get_by_name(username)
        if user is None:
            return None

        hsh = hashlib.sha256()
        hsh.update(bytes(raw_password, "utf-8") + user.salt)
        if user.sha256_password == hsh.digest():
            return user.id
        return None
