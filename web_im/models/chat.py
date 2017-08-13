import datetime
import sqlalchemy
import sqlalchemy.orm.exc
from web_im.exts import db


class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, index=True)
    recipient = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, index=True)
    body = db.Column(db.Text(140))

    def __init__(self, sender, recipient, body, timestamp):
        self.sender = sender
        self.recipient = recipient
        self.body = body
        self.timestamp = timestamp

    @classmethod
    def create(cls, sender, recipient, body, timestamp=None):
        """
        TODO update unread count
        """
        if timestamp is None:
            timestamp = datetime.datetime.utcnow()
        msg = cls(sender, recipient, body, timestamp)
        db.session.add(msg)

        try:
            db.session.commit()
            db.session.flush()
            return msg.id
        except BaseException as exc:
            db.session.rollback()
            raise exc

    @classmethod
    def get_many_by_user_pair(cls, sender_id, recipient_id):
        # TODO pagnize
        messages = db.session.query(
            cls
        ).filter(
            ((cls.recipient == sender_id) & (cls.sender == recipient_id)) |
            ((cls.recipient == recipient_id) & (cls.sender == sender_id))
        ).order_by(
            cls.timestamp.asc()
        ).all()
        return messages

    @classmethod
    def delete(cls, sender_id, message_id):
        cls.query.filter(
            (cls.sender == sender_id) & (cls.id == message_id)
        ).delete()

        try:
            db.session.commit()
        except BaseException as exc:
            db.session.rollback()
            raise exc


class UnreadMessageCount(db.Model):
    """
    unread count for recipient
    TODO: use redis-like KV storage with key "{sender}:{recipient}"
    """

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, index=True)
    recipient = db.Column(db.Integer, index=True)
    unread_count = db.Column(db.Integer, default=0)

    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            'sender', 'recipient', name='_unread_message_count'
        ),
    )

    def __init__(self, sender, recipient, unread_count=0):
        self.sender = sender
        self.recipient = recipient
        self.unread_count = unread_count

    @classmethod
    def get_unread(cls, sender_id, recipient_id):
        try:
            return db.session.query(
                cls.unread_count
            ).filter(
                (cls.sender == sender_id) & (cls.recipient == recipient_id)
            ).one()[0]
        except sqlalchemy.orm.exc.NoResultFound:
            return 0

    @classmethod
    def add_unread(cls, sender_id, recipient_id):
        n_changed = cls.query.filter(
            (cls.sender == sender_id) & (cls.recipient == recipient_id)
        ).update({
            "unread_count": cls.unread_count + 1
        })

        if n_changed == 0:
            obj = cls(sender_id, recipient_id, 1)
            db.session.add(obj)

        try:
            db.session.commit()
        except BaseException as exc:
            db.session.rollback()
            raise exc

    @classmethod
    def reset_unread(cls, sender_id, recipient_id):
        cls.query.filter(
            (cls.sender == sender_id) & (cls.recipient == recipient_id)
        ).update({
            "unread_count": 0
        })

        try:
            db.session.commit()
        except BaseException as exc:
            db.session.rollback()
            raise exc
