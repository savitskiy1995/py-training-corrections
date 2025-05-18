from fixture.orm import ORMfixture
from model.group import Group
from model.contact import Contact

import random

db = ORMfixture(host='127.0.0.1', name='addressbook', user='root', password='')


def test_delete_contact_to_group(app):
        if len(db.get_contact_list()) == 0:
            app.contact.create(Contact(firstname="Ilon", lastname="Mozg"))
        if len(db.get_group_list()) == 0:
            app.group.create(Group(name="Test"))
        old_contacts = db.get_contact_list()
        old_groups = db.get_group_list()
        contact_id = random.choice(old_contacts).id
        group_id = random.choice(old_groups).id
        if len(db.get_contacts_in_group(Group(id='%s' % group_id))) == 0:
            app.contact.add_contact_to_group(contact_id, group_id)
        old_contacts_in_group = db.get_contacts_in_group(Group(id='%s' % group_id))
        app.contact.delete_contact_from_group(group_id)
        new_contacts_in_group = db.get_contacts_in_group(Group(id='%s' % group_id))
        assert len(old_contacts_in_group) - 1 == len(new_contacts_in_group)