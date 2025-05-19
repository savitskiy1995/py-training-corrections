from fixture.orm import ORMfixture
from model.group import Group
from model.contact import Contact
import random
import pytest
import time


def test_add_contact_to_group(app, orm):
    # 1. Подготовка данных
    if not orm.get_contact_list():
        app.contact.create_contact(Contact(firstname="Test", lastname="Contact"))
    if not orm.get_group_list():
        app.group.create(Group(name="Test Group"))

    # 2. Выбор группы и контакта
    groups = orm.get_group_list()
    group = random.choice(groups)

    # Находим контакт, которого нет в группе
    contacts_not_in_group = orm.get_contacts_not_in_group(group)
    if contacts_not_in_group:
        contact = random.choice(contacts_not_in_group)
    else:
        # Если все контакты уже в группе, создаём новый
        app.contact.create_contact(Contact(firstname="New", lastname="Contact"))
        contact = orm.get_contact_list()[-1]

    # 3. Добавляем контакт в группу через интерфейс
    app.contact.add_contact_in_group(contact.id, group.id)

    # 4. Проверяем, что контакт добавился (через ORM)
    new_contacts_in_group = orm.get_contacts_in_group(group)

    assert contact.id in [c.id for c in new_contacts_in_group], \
        f"Контакт с ID {contact.id} не найден в группе {group.id}"
