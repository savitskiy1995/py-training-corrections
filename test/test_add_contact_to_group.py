from fixture.orm import ORMfixture
from model.group import Group
from model.contact import Contact
import random

db = ORMfixture(host='127.0.0.1', name='addressbook', user='root', password='')


def test_add_contact_to_group(app):
    if len(db.get_contact_list()) == 0:
        app.contact.create_contact(Contact(firstname="Name", lastname="Lastname"))
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="Test"))


    old_contacts = db.get_contact_list()
    old_groups = db.get_group_list()
    contact_from_old = random.choice(old_contacts)
    group_from_old = random.choice(old_groups)
    old_contacts_in_group = db.get_contacts_in_group(group_from_old)
    if len(db.get_contact_list()) == len(old_contacts_in_group):
            app.contact.create_contact(Contact(firstname="Michael", lastname="Jordan"))
    app.contact.add_contact_to_group(contact_from_old, group_from_old)
    new_contacts_in_group = db.get_contacts_in_group(group_from_old)
    assert len(old_contacts_in_group) + 1 == len(new_contacts_in_group)
    old_contacts_in_group.append(contact_from_old)
    assert sorted(old_contacts_in_group, key=Contact.id_or_max) == sorted(new_contacts_in_group, key=Contact.id_or_max)











