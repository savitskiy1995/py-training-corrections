import random

from model.group import Group


def test_delete_group(app, db, check_ui):
    old_groups = db.get_group_list_from_db()
    group = random.choice(old_groups)
    app.group.delete_group_by_index(group.id)
    new_groups = db.get_group_list_from_db()
    assert len(old_groups) - 1 == len(new_groups)
    old_groups.remove(group)
    assert old_groups == new_groups
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)
