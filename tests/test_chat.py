from testing_utils import BaseTestCase
from web_im.models.chat import Message, UnreadMessageCount


class MessageTestCase(BaseTestCase):

    def test_create(self):
        a = Message.get_many_by_user_pair(1, 2)
        b = Message.get_many_by_user_pair(2, 1)
        assert not a and not b

        Message.create(1, 2, "1 to 2")
        a = Message.get_many_by_user_pair(1, 2)
        b = Message.get_many_by_user_pair(2, 1)
        assert len(a) == 1
        assert a == b

        Message.create(2, 1, "2 to 1")
        assert Message.get_many_by_user_pair(1, 2) == \
            Message.get_many_by_user_pair(2, 1)

        a = Message.get_many_by_user_pair(1, 2)
        b = Message.get_many_by_user_pair(2, 1)
        assert len(a) == 2
        assert a == b

    def test_delete(self):
        msg_id1 = Message.create(1, 2, "1 to 2")
        Message.delete(2, msg_id1)
        a = Message.get_many_by_user_pair(1, 2)
        assert len(a) == 1

        Message.delete(1, msg_id1)
        a = Message.get_many_by_user_pair(1, 2)
        assert len(a) == 0


class UnreadMsgCountTestCase(BaseTestCase):

    def test_crud(self):
        UnreadMessageCount.add_unread(1, 2)
        n_unread = UnreadMessageCount.get_unread(1, 2)
        assert n_unread == 1
