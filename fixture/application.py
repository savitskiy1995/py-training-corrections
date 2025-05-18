from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from fixture.contact import ContactHelper
from fixture.group import GroupHelper
from fixture.session import SessionHelper


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)


    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.wd, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            raise AssertionError(f"Element not found: {by}={value}")


    def open_home_page(self):
        wd = self.wd
        wd.get("http://localhost/addressbook/")

    def destroy(self):
        self.wd.quit()
