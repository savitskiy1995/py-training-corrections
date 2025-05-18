from fixture.orm import ORMfixture
from model.group import Group
from model.contact import Contact
import random

db = ORMfixture(host='127.0.0.1', name='addressbook', user='root', password='')


def test_add_contact_to_group(app, orm):
    if len(db.get_contact_list()) == 0:
        app.contact.create_contact(Contact(firstname="Name", lastname="Lastname"))
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="Test"))

    groups = orm.get_group_list()
    contacts = orm.get_contact_list()
    group_contacts = []
    group_to_add = random.choice(groups)
    contact_for_add = None

    for group in groups:
        group_contacts.extend(orm.get_contacts_in_group(group))

    for contact in contacts:
        if contact not in group_contacts:
            contact_for_add = contact
            break

    if contact_for_add is None:
        app.contact.create_contact(Contact(firstname="Test", lastname="Testovich"))
        contact_for_add = orm.get_contact_list()[-1]

    app.contact.add_contact_in_group(contact_for_add.id, group_to_add.id)
    contacts_in_group = orm.get_contacts_in_group(group_to_add)
    assert contact_for_add.id in [c.id for c in contacts_in_group]








