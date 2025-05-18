from random import randrange

from model.group import Group


def test_delete_some_group(app, db, check_ui):
    old_groups = db.get_group_list_from_db()
    index = randrange(len(old_groups))
    app.group.delete_group_by_index(index)
    new_groups = db.get_group_list_from_db()
    assert len(old_groups) - 1 == len(new_groups)
    old_groups[index:index+1] = []
    assert old_groups == new_groups
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)
