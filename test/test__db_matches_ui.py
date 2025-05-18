from model.contact import Contact
from model.group import Group


def test_groups_from_db_matches_groups_from_ui(app, db):
    def clean(group):
        return Group(id=group.id, name=group.name.strip())
    ui_list = app.group.get_group_list()
    db_list = map(clean, db.get_group_list_from_db())
    assert sorted(ui_list, key=Group.id_or_max) == sorted(db_list, key=Group.id_or_max)


def test_contacts_from_db_matches_contacts_from_ui(app, db):
    ui_list = app.contact.get_contact_list()
    db_list = db.get_contact_list_from_db()
    assert sorted(ui_list, key=Contact.id_or_max) == sorted(db_list, key=Contact.id_or_max)