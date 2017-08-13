import pytest
import sqlalchemy.exc
from testing_utils import BaseTestCase
from web_im.models.user import User, ContactRelation


class UserTestCase(BaseTestCase):

    def test_create(self):
        uid1 = User.create("jack", "password")
        assert uid1 is not None
        with pytest.raises(sqlalchemy.exc.IntegrityError):
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


class ContactRelationTestCase(BaseTestCase):

    def test_connect(self):
        id1 = ContactRelation.connect(1, 2)
        assert ContactRelation.is_contact(1, 2)
        assert ContactRelation.is_contact(2, 1)
        assert id1 is not None
        None is ContactRelation.connect(2, 1)
        id2 = ContactRelation.connect(3, 2)
        assert id2 is not None
        assert ContactRelation.is_contact(2, 3)
        assert ContactRelation.is_contact(3, 2)

    def test_disconnect(self):
        ContactRelation.connect(1, 2)
        assert ContactRelation.is_contact(2, 1)
        ContactRelation.disconnect(2, 1)
        assert not ContactRelation.is_contact(2, 1)

    def test_retrieval(self):
        ContactRelation.connect(1, 2)
        assert [2] == ContactRelation.get_contact_ids(1)
        assert [1] == ContactRelation.get_contact_ids(2)
        ContactRelation.connect(1, 3)
        assert {2, 3} == set(ContactRelation.get_contact_ids(1))
        assert [1] == ContactRelation.get_contact_ids(2)
        assert [1] == ContactRelation.get_contact_ids(3)
        assert [] == ContactRelation.get_contact_ids(999)


class ContactsTestCase(BaseTestCase):

    def test_contacts(self):
        jack_id = User.create("jack", "password")
        rose_id = User.create("rose", "password")
        ContactRelation.connect(jack_id, rose_id)
        jack = User.get(jack_id)
        jack.get_contacts()
