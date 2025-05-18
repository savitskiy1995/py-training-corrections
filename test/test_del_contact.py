from random import randrange

from model.contact import Contact


def test_del_contact(app, db, check_ui):
    old_contacts = db.get_contact_list_from_db()
    index = randrange(len(old_contacts))
    contact = old_contacts[index]
    app.contact.delete_contact_by_id(contact.id)
    new_contacts = db.get_contact_list_from_db()
    assert len(old_contacts) - 1 == len(new_contacts)
    old_contacts[index:index+1] = []
    assert old_contacts == new_contacts
    if check_ui:
        assert sorted(old_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(),
                                                                     key=Contact.id_or_max)

