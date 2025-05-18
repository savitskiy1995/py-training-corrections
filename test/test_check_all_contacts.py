import re
from random import randrange
from model.contact import Contact

def test_check_all_contact(app, db):
    contact_from_home_page = sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
    contact_from_db = sorted(db.get_contact_list(), key=Contact.id_or_max)

    for c in range(len(contact_from_home_page)):
        assert contact_from_home_page[c].all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_db[c])
        assert contact_from_home_page[c].all_email_from_home_page == merge_email_like_on_home_page(contact_from_db[c])
        assert contact_from_home_page[c].address == contact_from_db[c].address
        assert clear_text(contact_from_home_page[c].firstname) == clear_text(contact_from_db[c].firstname)
        assert clear_text(contact_from_home_page[c].lastname) == clear_text(contact_from_db[c].lastname)

    index = randrange(len(app.contact.get_contact_list()))
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    contact_from_view_page = app.contact.get_contact_from_view_page(index)

    assert contact_from_view_page.home_phone == contact_from_edit_page.home_phone
    assert contact_from_view_page.mobilephone == contact_from_edit_page.mobilephone
    assert contact_from_view_page.secondaryphone == contact_from_edit_page.secondaryphone
    assert contact_from_view_page.workphone == contact_from_edit_page.workphone

    assert contact_from_view_page.email == contact_from_edit_page.email
    assert contact_from_view_page.email2 == contact_from_edit_page.email2
    assert contact_from_view_page.email3 == contact_from_edit_page.email3

    assert contact_from_view_page.address == contact_from_edit_page.address

    assert clear_text(contact_from_view_page.firstname) == clear_text(contact_from_edit_page.firstname)
    assert clear_text(contact_from_view_page.lastname) == clear_text(contact_from_edit_page.lastname)

def clear_text(s):
    return re.sub(r"\s+", "", s)

def clear_phone(s):
    return re.sub(r"[() -]", "", s)

def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "", map(lambda x: clear_phone(x), filter(lambda x: x is not None, [contact.home, contact.mobile, contact.work, contact.fax]))))

def merge_email_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "", map(lambda x: clear_text(x), filter(lambda x: x is not None, [contact.email, contact.email2, contact.email3]))))