

class Session(object):
    USERNAME = 'Auth.username'
    USERID = 'Auth.userid'
    PAGEMESSAGE = 'Auth.pagemessage'

    def __init__(self, session):
        self.session = session

    @property
    def username(self):
        if not self.session:
            return None
        name = self.session.get(self.USERNAME, None)
        return name

    @property
    def user_id(self):
        if not self.session:
            return None
        return self.session.get(self.USERID, None)

    @property
    def page_message(self):
        if not self.session:
            return None
        return self.session.get(self.PAGEMESSAGE, None)

    def set_page_message(self, message):
        self.session[self.PAGEMESSAGE] = message

    def is_logged_in(self):
        username_exist = self.USERNAME in self.session
        user_id_exist = self.USERID in self.session
        if username_exist and user_id_exist:
            return True

        return False

    def login(self, user_id, username):
        self.session[self.USERID] = user_id
        self.session[self.USERNAME] = username

    def logout(self):
        del self.session[self.USERNAME]
        del self.session[self.USERID]
