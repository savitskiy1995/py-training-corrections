from fixture.orm import ORMfixture
from model.group import Group
from model.contact import Contact

import random

db = ORMfixture(host='127.0.0.1', name='addressbook', user='root', password='')


def test_del_contact_in_group(app, orm):
    if len(orm.get_contact_list()) == 0:
        app.contact.create_contact(Contact(firstname="Name", lastname="Lastname"))
    if len(orm.get_group_list()) == 0:
        app.group.create(Group(name="Test"))

    all_groups = orm.get_group_list()
    contacts_with_groups = []

    for group in all_groups:
        group_contacts = orm.get_contacts_in_group(group)
        if group_contacts:
            selected_contact = random.choice(group_contacts)
            contacts_with_groups.append((selected_contact, group))

    if not contacts_with_groups:
        random_contact = random.choice(orm.get_contact_list())
        random_group = random.choice(all_groups)
        app.contact.add_contact_in_group(random_contact.id, random_group.id)
        contacts_with_groups.append((random_contact, random_group))

    contact_to_remove, target_group = random.choice(contacts_with_groups)
    app.contact.delete_contact_in_group(contact_to_remove.id, target_group.id)

    contacts_not_in_group = orm.get_contacts_not_in_group(target_group)
    assert contact_to_remove.id in [c.id for c in contacts_not_in_group]