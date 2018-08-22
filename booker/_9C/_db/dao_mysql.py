from mysql_engine import mysqlEngne
import logging


class DaoMysql(object):

    logger = logging.getLogger()

    @staticmethod
    def get_available_account():
        with mysqlEngne as db:
            try:
                db.cursor.execute("SELECT * FROM account_9c WHERE is_disabled = 0 order by rand() limit 1")
                results = db.cursor.fetchone()
                username = results[1]
                password = results[2]
                logging.info("user:%s", username)
                return {
                    "username": username,
                    "password": password
                }
            except:
                logging.info("Error in querying the database")
                return {}

    @staticmethod
    def change_account_disabled(username):
        with mysqlEngne as db:
            try:
                db.cursor.execute(
                    "UPDATE account_9c SET is_disabled = 1,gmt_modified = now() WHERE username = '%s'" % username)
            except:
                logging.info("Error in update the database")
