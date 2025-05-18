from selenium.webdriver.common.by import By

from model.group import Group


class GroupHelper:

    group_cache = None

    def __init__(self, app):
        self.app = app


    def return_to_groups_page(self):
        wd = self.app.wd
        self.app.wait_for_element(By.LINK_TEXT, "group page").click()


    def create(self, group):
        wd = self.app.wd
        self.open_group_page()
        # init group creation
        self.open_new_group_page()
        self.fill_group_form(group)
        # submit group creation
        self.app.wait_for_element(By.NAME, "submit").click()
        self.return_to_groups_page()
        self.group_cache = None

    def open_group_page(self):
        wd = self.app.wd
        if wd.current_url.endswith("/group.php") and len (wd.find_elements(By.NAME, "new")) > 0:
            return
        self.app.wait_for_element(By.LINK_TEXT, "groups").click()


    def delete_first_group(self):
        wd = self.app.wd
        self.delete_group_by_index(0)


    def select_group_by_index(self, index):
        wd = self.app.wd
        wd.find_elements(By.NAME, "selected[]")[index].click()


    def delete_group_by_index(self, index):
        wd = self.app.wd
        self.open_group_page()
        if not self.is_group_exist():
            self.open_new_group_page()
            self.create(Group(name="New group", header="New header"))
        self.select_group_by_index(index)
        self.app.wait_for_element(By.NAME, "delete").click()
        self.return_to_groups_page()
        self.group_cache = None


    def count(self):
        wd = self.app.wd
        self.open_group_page()
        return len(wd.find_elements(By.NAME, "selected[]"))


    def edit_first_group(self):
        wd = self.app.wd
        self.edit_group_by_index(0)


    def edit_group_by_index(self, group, index):
        wd = self.app.wd
        self.open_group_page()
        if not self.is_group_exist():
            self.open_new_group_page()
            self.create(group)
        self.select_group_by_index(index)
        self.app.wait_for_element(By.NAME, "edit").click()
        self.fill_group_form(group)
        # submit group creation
        self.app.wait_for_element(By.NAME, "update").click()
        self.return_to_groups_page()
        self.group_cache = None


    def open_new_group_page(self):
        self.app.wait_for_element(By.NAME, "new").click()


    def fill_group_form(self, group):
        group_name = self.app.wait_for_element(By.NAME, "group_name")
        group_name.click()
        group_name.clear()
        group_name.send_keys(group.name if group.name else "")

        group_header = self.app.wait_for_element(By.NAME, "group_header")
        group_header.click()
        group_header.clear()
        group_header.send_keys(group.header if group.header else "")


    def is_group_exist(self):
        wd = self.app.wd
        return len(wd.find_elements(By.NAME, "selected[]")) > 0


    def get_group_list(self):
        if self.group_cache is None:
            wd = self.app.wd
            self.open_group_page()
            self.group_cache = []
            for element in wd.find_elements(By.CSS_SELECTOR, "span.group"):
                # Получаем input внутри span
                input_element = element.find_element(By.NAME, "selected[]")
                # Значение атрибута value (ID группы)
                id = input_element.get_attribute("value")
                # Текст из title атрибута (название группы)
                name = input_element.get_attribute("title").replace("Select (", "").replace(")", "")
                self.group_cache.append(Group(name=name, id=id))
        return list(self.group_cache)
