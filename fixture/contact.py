import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

from model.contact import Contact


class ContactHelper:

    def __init__(self, app):
        self.app = app


    contacts_cache = None

    def count(self):
        wd = self.app.wd
        return len(wd.find_elements(By.NAME, "selected[]"))


    def create_contact(self, contact):
        wd = self.app.wd
        self.open_add_contact_page()
        # fill contact form
        self.fill_contact_form(contact)
        # submit contact creation
        self.app.wait_for_element(By.XPATH, "//div[@id='content']/form/input[20]").click()
        self.return_to_home_page()
        self.contacts_cache = None

    def fill_contact_form(self, contact):
        firstname_field = self.app.wait_for_element(By.NAME, "firstname")
        firstname_field.clear()
        if contact.firstname:
            firstname_field.send_keys(contact.firstname)

        lastname_field = self.app.wait_for_element(By.NAME, "lastname")
        lastname_field.clear()
        if contact.lastname:
            lastname_field.send_keys(contact.lastname)

        #company_field = self.app.wait_for_element(By.NAME, "company")
        #company_field.clear()
        #if contact.company:
        #    company_field.send_keys(contact.company)

        home_phone_field = self.app.wait_for_element(By.NAME, "home")
        home_phone_field.clear()
        if contact.home_phone:
            home_phone_field.send_keys(contact.home_phone)

        email_field = self.app.wait_for_element(By.NAME, "email")
        email_field.clear()
        if contact.email:
            email_field.send_keys(contact.email)

    def add_contact_to_group(self, contact_id, group_id):
        wd = self.app.wd
        self.open_contacts_homepage()
        wd.find_element(By.CSS_SELECTOR,"input[value='%s']" % contact_id).click()
        select = Select(wd.find_element(By.CSS_SELECTOR,"select[name='to_group']"))
        select.select_by_value('%s' % group_id)
        wd.find_element(By.CSS_SELECTOR,"input[value='Add to']").click()
        wd.find_element(By.CSS_SELECTOR,"a[href='./?group=%s']" % group_id).click()

    def delete_contact_from_group(self, group_id):
        wd = self.app.wd
        self.open_contacts_homepage()
        select = Select(wd.find_element(By.CSS_SELECTOR,"select[name='group']"))
        select.select_by_value('%s' % group_id)
        wd.find_element(By.CSS_SELECTOR,"input[name='selected[]']").click()
        wd.find_element(By.CSS_SELECTOR,"input[name='remove']").click()
        wd.find_element(By.CSS_SELECTOR,"a[href='./?group=%s']" % group_id).click()

    def delete_contact_by_id(self, id):
        wd = self.app.wd
        self.open_contacts_homepage()
        self.select_contact_by_id(id)
        wd.find_element(By.CSS_SELECTOR,"input[value='Delete']").click()
        wd.switch_to_alert().accept()
        self.open_contacts_homepage()
        self.contact_cache = None

    def edit_contact_by_id(self, id, new_contact_data):
        wd = self.app.wd
        self.open_contacts_homepage()
        wd.find_element(By.CSS_SELECTOR,"a[href='edit.php?id=%s']" % id).click()
        self.fill_contact_form(new_contact_data)
        wd.find_element_by_name("update").click()
        self.open_contacts_homepage()
        self.contact_cache = None

    def select_contact_by_id(self, id):
        wd = self.app.wd
        wd.find_element(By.CSS_SELECTOR,"input[value='%s']" % id).click()

    def edit_contact_by_index(self, contact, index):
        wd = self.app.wd
        if not self.is_contact_exist():
            self.open_add_contact_page()
            self.create_contact(contact)
        self.open_edit_contact_by_index(index)
        self.fill_contact_form(contact)
        self.app.wait_for_element(By.XPATH, "//input[@value='Update']").click()
        self.contacts_cache = None
        self.return_to_home_page()


    def open_add_contact_page(self):
        wd = self.app.wd
        if wd.current_url.endswith("/edit.php") and len (wd.find_elements(By.NAME, "Enter")) > 0:
            return
        self.app.wait_for_element(By.LINK_TEXT, "add new").click()


    def open_contacts_homepage(self):
        wd = self.app.wd
        if not wd.current_url.endswith("addressbook/"):
            wd.find_element(By.LINK_TEXT,"home").click()


    def return_to_home_page(self):
        self.app.wait_for_element(By.LINK_TEXT, "home page").click()

    def delete_first_contact(self):
        wd = self.app.wd
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        if not self.is_contact_exist():
            self.open_add_contact_page()
            self.create_contact(Contact(
                firstname="John",
                lastname="Smith",
                company="Google",
                home_phone="+7999999999",
                email="johnsmith@gmail.com"
            ))
        self.open_edit_contact_by_index(index)
        self.app.wait_for_element(By.XPATH, "//input[@value='Delete']").click()
        self.contacts_cache = None


    def open_edit_contact_by_index(self, index):
        wd = self.app.wd
        if not wd.current_url.endswith("addressbook/"):
            wd.find_element(By.XPATH, "//a[contains(.,'home')]").click()
        wd.find_elements(By.XPATH, "//img[@title='Edit']")[index].click()


    def edit_first_contact(self, contact):
        wd = self.app.wd
        wd.edit_contact_by_index(contact, 0)


    def is_contact_exist(self):
        wd = self.app.wd
        return len(wd.find_elements(By.NAME, "selected[]")) > 0

    def get_contact_list(self):
        if self.contacts_cache is None:
            wd = self.app.wd
            self.contacts_cache = []
            self.app.wait_for_element(By.NAME, "entry")
            for element in wd.find_elements(By.NAME, "entry"):
                cells = element.find_elements(By.TAG_NAME, "td")
                id = element.find_element(By.TAG_NAME, "input").get_attribute("value")
                last_name = cells[1].text
                first_name = cells[2].text
                address = cells[3].text
                email = cells[4].text
                all_phones = cells[5].text

                email = email if email else None
                all_phones = all_phones if all_phones else None

                self.contacts_cache.append(Contact(
                    id=id,
                    firstname=first_name,
                    lastname=last_name,
                    address=address,
                    all_emails_from_home_page=email,
                    all_phones_from_home_page=all_phones
                ))
        return list(self.contacts_cache)

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_edit_contact_by_index(index)
        firstname = wd.find_element(By.NAME, "firstname").get_attribute("value")
        lastname = wd.find_element(By.NAME, "lastname").get_attribute("value")
        id = wd.find_element(By.NAME, "id").get_attribute("value")
        homephone = wd.find_element(By.NAME, "home").get_attribute("value")
        workphone = wd.find_element(By.NAME, "work").get_attribute("value")
        mobilephone = wd.find_element(By.NAME, "mobile").get_attribute("value")
        address = wd.find_element(By.NAME,"address").get_attribute("value")
        email = wd.find_element(By.NAME,"email").get_attribute("value")
        email2 = wd.find_element(By.NAME,"email2").get_attribute("value")
        email3 = wd.find_element(By.NAME,"email3").get_attribute("value")
        return Contact (firstname=firstname, lastname=lastname, id=id, home_phone=homephone,
                        workphone=workphone, mobilephone=mobilephone,
                        address=address, email=email, email2=email2, email3=email3)



    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.open_home_page()
        row = wd.find_elements(By.NAME, "entry")[index]
        cell = row.find_elements(By.TAG_NAME, "td")[6]
        cell.find_element(By.TAG_NAME, "a").click()
    
    
    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        text = wd.find_element(By.ID, "content").text
        # Ищем номера, но если не находим — возвращаем пустую строку
        homephone_match = re.search(r"H: (.*)", text)
        workphone_match = re.search(r"W: (.*)", text)
        mobilephone_match = re.search(r"M: (.*)", text)

        homephone = homephone_match.group(1) if homephone_match else ""
        workphone = workphone_match.group(1) if workphone_match else ""
        mobilephone = mobilephone_match.group(1) if mobilephone_match else ""

        return Contact(
            home_phone=homephone,
            workphone=workphone,
            mobilephone=mobilephone
        )

    def open_home_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("addressbook/"):
            wd.find_element(By.XPATH, "//a[contains(.,'home')]").click()
