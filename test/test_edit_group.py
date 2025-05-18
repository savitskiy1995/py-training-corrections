from random import randrange

from model.group import Group

def test_edit_group(app, db, check_ui):
    old_groups = db.get_group_list_from_db()
    index = randrange(len(old_groups))
    group = Group(name="Edit group", header="Edit header")
    group.id = old_groups[index].id
    app.group.edit_group_by_index(group, index)
    new_groups = db.get_group_list_from_db()
    assert len(old_groups) == len(new_groups)
    old_groups[index] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)