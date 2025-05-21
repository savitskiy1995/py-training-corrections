import random
from random import randrange

from model.group import Group

def test_edit_group(app, db, check_ui):
    old_groups = db.get_group_list_from_db()
    group = random.choice(old_groups)
    new_group = Group(name="Edit group", header="Edit header")
    app.group.edit_group_by_index(group, group.id)
    new_groups = db.get_group_list_from_db()
    assert len(old_groups) == len(new_groups)
    new_group.id = group.id
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)