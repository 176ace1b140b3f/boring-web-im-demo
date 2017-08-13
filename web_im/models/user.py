import os
import itertools
import hashlib
import sqlalchemy
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

    def get_contacts(self):
        # TODO return model instead of tuple
        contact_ids = ContactRelation.get_contact_ids(self.id)
        contacts = db.session.query(
            User.id, User.name
        ).filter(
            User.id.in_(contact_ids)
        ).all()
        return contacts


class ContactRelation(db.Model):
    """
    TODO: use nosql db
    user_id_a < user_id_b
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id_a = db.Column(db.Integer)
    user_id_b = db.Column(db.Integer)
    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            'user_id_a', 'user_id_b', name='_user_id_pair'
        ),
    )

    @classmethod
    def connect(cls, user_id_a, user_id_b):
        if user_id_a == user_id_b:
            return None
        if user_id_a > user_id_b:
            user_id_a, user_id_b = user_id_b, user_id_a

        rel = cls()
        rel.user_id_a = user_id_a
        rel.user_id_b = user_id_b

        db.session.add(rel)
        try:
            db.session.commit()
            db.session.flush()
            return rel.id
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def disconnect(cls, user_id_a, user_id_b):
        if user_id_a == user_id_b:
            return

        if user_id_a > user_id_b:
            user_id_a, user_id_b = user_id_b, user_id_a

        cls.query.filter(
            (cls.user_id_a == user_id_a) &
            (cls.user_id_b == user_id_b)
        ).delete()

        try:
            db.session.commit()
            db.session.flush()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()

    @classmethod
    def is_contact(cls, user_id_a, user_id_b):
        if user_id_a == user_id_b:
            return False
        if user_id_a > user_id_b:
            user_id_a, user_id_b = user_id_b, user_id_a

        try:
            db.session.query(cls).filter(
                (cls.user_id_a == user_id_a) &
                (cls.user_id_b == user_id_b)
            ).one()
            return True
        except sqlalchemy.orm.exc.NoResultFound:
            return False

    @classmethod
    def get_contact_ids(cls, user_id):
        part1 = db.session.query(cls.user_id_a). \
            filter(cls.user_id_b == user_id)
        part2 = db.session.query(cls.user_id_b). \
            filter(cls.user_id_a == user_id)
        return [id_ for id_, in itertools.chain(part1, part2)]
