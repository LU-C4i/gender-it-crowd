#!/usr/bin/env python2.7
# encoding: utf-8
'''Implement authentication using bcrypt and MySQLdb

See also:
    https://pypi.python.org/pypi/bcrypt/1.0.1
'''
import model
import MySQLdb
import bcrypt


class Repository(model.Model):
    def __init__(self, dbhost, dbuser, dbpass, dbname, port, session=None):
        '''

        :type session: dict like object for storing sessions.
        '''
        super(self.__class__, self).__init__(dbhost, dbuser, dbpass, dbname, port=port)
        self.session = session

    def get_user(self, username):
        query = "SELECT * FROM t_usr_user WHERE LOWER(usr_login) = %s"
        self.execute(query, (username.lower(),))
        return self.fetchone()

    def register(self, username, password):
        username = username.lower()
        hashed = None
        salt = bcrypt.gensalt(10)
        if password is not None:
            hashed = bcrypt.hashpw(password, salt)
        try:
            self.execute("INSERT INTO t_usr_user (usr_login, usr_password) VALUES (%s, %s)",
                         (username, hashed))
        except MySQLdb.IntegrityError:
            return False, 0
        user_id = self.insert_id()
        self.commit()
        return True, user_id

    def check_login(self, username, password):
        user = self.get_user(username)
        if user is None:
            return False, 0

        hashed = user['usr_password']
        if hashed is not None and bcrypt.checkpw(password, hashed):
            return True, user['usr_id']

        return False, 0

    def save_user_prediction(self, user_id, twitter_id, prediction):
        if self.fetch_prediction(user_id, twitter_id) is None:
            self.execute("INSERT INTO t_cpr_crowdprediction (cpr_usr_id, cpr_tus_id, cpr_prediction) VALUES (%s, %s, %s)"
                         , (user_id, twitter_id, prediction))
            self.commit()
        else:
            self.update_user_prediction(user_id, twitter_id, prediction)
        return

    def update_user_prediction(self, user_id, twitter_id, prediction):
        self.execute("UPDATE t_cpr_crowdprediction SET cpr_prediction = %s WHERE cpr_usr_id = %s AND cpr_tus_id = %s"
                     , (prediction, user_id, twitter_id))
        self.commit()

    def fetch_prediction(self, user_id, twitter_id):
        self.execute("SELECT * FROM t_cpr_crowdprediction WHERE cpr_usr_id = %s AND cpr_tus_id = %s"
                     , (user_id, twitter_id))
        return self.fetchone()

    def fetch_twitter_user(self, twitter_user_id):
        self.execute("SELECT * FROM t_tus_twitteruser WHERE tus_id = %s", (twitter_user_id,))
        return self.fetchone()

    not_more_than_x_predictions = 3

    def fetch_next_twitter_user(self, user_id):
        self.execute("SELECT * FROM t_tus_twitteruser t WHERE tus_id NOT IN (SELECT cpr_tus_id FROM t_cpr_crowdprediction WHERE cpr_usr_id = %s) AND (SELECT COUNT(cpr_id) FROM t_cpr_crowdprediction WHERE cpr_tus_id = t.tus_id AND cpr_prediction <> 'skipped') < %s LIMIT 1"
                     , (user_id, self.not_more_than_x_predictions))
        return self.fetchone()

    def fetch_progress(self):
        #self.execute("SELECT COUNT(*) as 'count' FROM t_tus_twitteruser")
        #total_amount = self.fetchone()
        self.execute("SELECT COUNT(*) as 'count' FROM t_cpr_crowdprediction WHERE cpr_prediction <> 'skipped'")
        total_predictions = self.fetchone()

        progress = (total_predictions['count']/(self.not_more_than_x_predictions*1.0)) / 20000.0
        return progress * 100

    def fetch_leaderboard(self):
        self.execute("SELECT usr_login, COUNT(*) AS score FROM t_cpr_crowdprediction INNER JOIN t_usr_user ON cpr_usr_id = usr_id WHERE cpr_prediction <> 'skipped' GROUP BY usr_login ORDER BY COUNT(*) DESC");
        return self.fetchall()
