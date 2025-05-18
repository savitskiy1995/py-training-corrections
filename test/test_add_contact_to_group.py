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

    # 3. Сохраняем текущее состояние группы
    old_contacts_in_group = orm.get_contacts_in_group(group)
    old_count = len(old_contacts_in_group)

    # 4. Добавляем контакт в группу через интерфейс
    app.contact.add_contact_in_group(contact.id, group.id)

    # 5. Проверяем, что контакт добавился (через ORM)
    new_contacts_in_group = orm.get_contacts_in_group(group)
    new_count = len(new_contacts_in_group)

    assert new_count == old_count + 1, \
        f"Количество контактов в группе не изменилось. Было: {old_count}, стало: {new_count}"

    assert contact.id in [c.id for c in new_contacts_in_group], \
        f"Контакт с ID {contact.id} не найден в группе {group.id}"

    # 6. Дополнительная проверка через интерфейс
    app.contact.open_home_page()
    app.contact.select_group_in_filter_by_id(group.id)
    ui_contacts = app.contact.get_contact_list()
    assert contact.id in [c.id for c in ui_contacts], \
        f"Контакт с ID {contact.id} не отображается в группе {group.id} в интерфейсе"