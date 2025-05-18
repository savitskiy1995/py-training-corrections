# -*- coding: utf-8 -*-
from model.contact import Contact


def test_add_contact(app, json_contacts, db, check_ui):
    contact = json_contacts
    old_contacts = db.get_contact_list_from_db()
    app.contact.create_contact(contact)
    new_contacts = db.get_contact_list_from_db()
    assert len(old_contacts) + 1 == len(new_contacts)
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(old_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(),
                                                                     key=Contact.id_or_max)
