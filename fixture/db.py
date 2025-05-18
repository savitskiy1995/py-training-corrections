import mysql.connector

from model.contact import Contact
from model.group import Group


class DbFixture:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = mysql.connector.connect(host=host, database=name, user=user, password=password)
        self.connection.autocommit = True

    def get_group_list_from_db(self):
        group_list_from_db = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_header from group_list")
            for row in cursor.fetchall():
                id = row[0]
                name = row[1]
                header = row[2]
                group_list_from_db.append(Group(id=str(id), name=name, header=header))
        finally:
            cursor.close()
        return group_list_from_db

    def get_contact_list_from_db(self):
        contact_list_from_db = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "select id, firstname, lastname, address, email from addressbook")
            for row in cursor.fetchall():
                (id, firstname, lastname, address, email) = row
                contact_list_from_db.append(
                    Contact(id=str(id), firstname=firstname, lastname=lastname, address=address, email=email))
        finally:
            cursor.close()
        return contact_list_from_db


    def destroy(self):
        self.connection.close()