import re
from random import randrange


def test_data_on_home_and_edit_pages(app):
    index = randrange(len(app.contact.get_contact_list()))
    data_on_home_page = app.contact.get_contact_list()[index]
    data_on_edit_page = app.contact.app.contact.get_contact_info_from_edit_page(index)
    assert data_on_home_page.firstname == data_on_edit_page.firstname
    assert data_on_home_page.lastname == data_on_edit_page.lastname
    assert data_on_home_page.address == data_on_edit_page.address
    assert data_on_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(data_on_edit_page)
    assert data_on_home_page.all_emails_from_home_page == merge_emails_like_on_home_page(data_on_edit_page)


def clear(s):
    return re.sub("[()-]", "", s)


def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "",
                             map(lambda x: clear(x), filter(lambda x: x is not None,
                            [contact.home_phone, contact.mobilephone, contact.workphone]))))


def merge_emails_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "", map(lambda x: clear(x), filter(lambda x: x is not None,
                            [contact.email, contact.email2, contact.email3]))))