from fixture.orm import ORMfixture
from model.group import Group
from model.contact import Contact
import random
import pytest


def test_del_contact_in_group(app, orm):
    # 1. Подготовка данных: создание контакта и группы, если их нет
    if not orm.get_contact_list():
        app.contact.create_contact(Contact(firstname="Test", lastname="Contact"))
    if not orm.get_group_list():
        app.group.create(Group(name="Test Group"))

    # 2. Выбор группы с контактами
    groups = orm.get_group_list()

    group = random.choice(groups)
    contact = random.choice(orm.get_contact_list())
    app.contact.add_contact_in_group(contact.id, group.id)
    contacts_in_group = [contact]

    # 3. Выбираем контакт для удаления из группы
    contact_to_remove = random.choice(contacts_in_group)


    # 5. Удаляем контакт из группы через интерфейс
    app.contact.delete_contact_in_group(contact_to_remove.id, group.id)

    # 6. Проверяем, что контакт удалился (через ORM)
    new_contacts_in_group = orm.get_contacts_in_group(group)


    assert contact_to_remove.id not in [c.id for c in new_contacts_in_group], \
        f"Контакт с ID {contact_to_remove.id} всё ещё находится в группе {group.id}"
