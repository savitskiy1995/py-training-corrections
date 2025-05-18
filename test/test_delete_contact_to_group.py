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
    group = None
    contacts_in_group = []

    # Ищем группу, в которой есть хотя бы один контакт
    for g in groups:
        contacts = orm.get_contacts_in_group(g)
        if contacts:
            group = g
            contacts_in_group = contacts
            break

    # Если нет группы с контактами, добавляем случайный контакт в случайную группу
    if not group:
        group = random.choice(groups)
        contact = random.choice(orm.get_contact_list())
        app.contact.add_contact_in_group(contact.id, group.id)
        contacts_in_group = [contact]

    # 3. Выбираем контакт для удаления из группы
    contact_to_remove = random.choice(contacts_in_group)

    # 4. Сохраняем текущее состояние группы
    old_contacts_in_group = orm.get_contacts_in_group(group)
    old_count = len(old_contacts_in_group)

    # 5. Удаляем контакт из группы через интерфейс
    app.contact.delete_contact_in_group(contact_to_remove.id, group.id)

    # 6. Проверяем, что контакт удалился (через ORM)
    new_contacts_in_group = orm.get_contacts_in_group(group)
    new_count = len(new_contacts_in_group)

    assert new_count == old_count - 1, \
        f"Количество контактов в группе не изменилось. Было: {old_count}, стало: {new_count}"

    assert contact_to_remove.id not in [c.id for c in new_contacts_in_group], \
        f"Контакт с ID {contact_to_remove.id} всё ещё находится в группе {group.id}"

    # 7. Дополнительная проверка через интерфейс
    app.contact.open_home_page()
    app.contact.select_group_in_filter_by_id(group.id)
    ui_contacts = app.contact.get_contact_list()
    assert contact_to_remove.id not in [c.id for c in ui_contacts], \
        f"Контакт с ID {contact_to_remove.id} отображается в группе {group.id} в интерфейсе"
