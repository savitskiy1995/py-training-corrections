from sys import maxsize


class Contact:
    def __init__(self, firstname=None, lastname=None, address=None, home_phone=None,
                 company = None, email=None, id=None, all_phones_from_home_page = None,
                 mobilephone=None, secondaryphone=None, workphone=None, all_emails_from_home_page = None,
                 email2 = None, email3 = None):
        self.firstname = firstname
        self.lastname = lastname
        self.company = company
        self.address = address
        self.home_phone = home_phone
        self.email = email
        self.id = id
        self.mobilephone = mobilephone
        self.secondaryphone = secondaryphone
        self.workphone = workphone
        self.all_phones_from_home_page = all_phones_from_home_page
        self.all_emails_from_home_page = all_emails_from_home_page
        self.email2 = email2
        self.email3 = email3


    def __repr__(self):
        return "%s:%s %s" % (self.id, self.firstname, self.lastname)


    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and (self.lastname, self.firstname) == (
            other.lastname, other.firstname)


    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize