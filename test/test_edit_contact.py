from random import randrange
import random

from model.contact import Contact

def test_edit_contact(app, db, check_ui):
    old_contacts = db.get_contact_list_from_db()
    contact = random.choice(old_contacts)
    some_new_contact = Contact(
        firstname="Victor",
        lastname="Douglas",
        company="Apple",
        home_phone="+7999999999",
        email="vic_douglas@me.com"
    )
    app.contact.edit_contact_by_id(contact.id, some_new_contact)
    new_contacts = db.get_contact_list_from_db()
    assert len(old_contacts) == len(new_contacts)
    some_new_contact.id = contact.id
    old_contacts = [c if c.id != contact.id else some_new_contact for c in old_contacts]
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(),
                                                                     key=Contact.id_or_max)