# -*- coding: UTF-8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB
from conf import booker_config
import logging


class PTConnectionPool(object):
    __pool = None
    logger = logging.getLogger()

    def __enter__(self):
        self.conn = self.getConn()
        self.cursor = self.conn.cursor()
        return self

    def getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(creator=pymysql, mincached=booker_config.getint("datasource", "DB_MIN_CACHED"),
                                   maxcached=booker_config.getint("datasource", "DB_MAX_CACHED"),
                                   maxshared=booker_config.getint("datasource", "DB_MAX_SHARED"),
                                   maxconnections=booker_config.getint("datasource", "DB_MAX_CONNECYIONS"),
                                   blocking=booker_config.getboolean("datasource", "DB_BLOCKING"),
                                   host=booker_config.get("datasource", "DB_HOST"),
                                   port=booker_config.getint("datasource", "DB_PORT"),
                                   user=booker_config.get("datasource", "DB_USER"),
                                   passwd=booker_config.get("datasource", "DB_PASSWORD"),
                                   db=booker_config.get("datasource", "DB_DBNAME"), use_unicode=False,
                                   charset=booker_config.get("datasource", "DB_CHARSET"),
                                   setsession=['SET AUTOCOMMIT = 1'])

        return self.__pool.connection()

    """
    @summary: 释放连接池资源
    """

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()
