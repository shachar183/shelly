# -------------------------------------------------------------------------------
# Message
# -------------------------------------------------------------------------------
# A class to manage the Messages - create and save in the DB
# -------------------------------------------------------------------------
# Author:       Dan Avrahami
# Last updated: 21.12.2015
# -------------------------------------------------------------------------

# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
import MySQLdb

import main

DAYS = {'Sunday':0, 'Monday':1, 'Tuesday':2, 'Wednesday':3,'Thursday':4 , 'Friday':5, 'Saturday':6}

class Account():
    global DAYS
    def __init__(self, email):
        self.d_DbHandler = db_handler.DbHandler()
        self.owner_email = email
        self.owner_first_name = ""
        self.owner_last_name = ""
        self.owner_full_name = ""
        self.owner_phone = ""
        self.dog_name = ""
        self.dog_gender = ""
        self.dog_type = ""
        self.owner_city = ""
        self.prefered_walking_days = ""
        self.dog_info = {}
        self.schedule = [[],[],[],[],[],[],[]]

    def insert_owner_detail(self):
        logging.info('starting insertion')
        self.d_DbHandler.connectToDb()
        cursor = self.d_DbHandler.getCursor()
        query = """
                INSERT INTO dog_owners(owner_email, first_name, last_name, phone_number, dog_name, dog_gender,
                                        dog_type, city_name) 
                VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
                """.format(self.owner_email, self.owner_first_name, self.owner_last_name, self.owner_phone,
                           self.dog_name, self.dog_gender, self.dog_type, self.owner_city)
        cursor.execute(query)
        logging.info('finished running query')
        self.d_DbHandler.commit()

        for day in self.prefered_walking_days:
            cursor = self.d_DbHandler.getCursor()
            query = """
                    INSERT INTO prefered_walking_days(owner_email, day_of_week)
                    VALUES('{0}','{1}')
                    """.format(self.owner_email, day)
            cursor.execute(query)
            logging.info('finished running query')
        self.d_DbHandler.commit()
        self.d_DbHandler.disconnectFromDb()
        logging.info('Finished insertion to DB!')

    def get_owner_detail(self):
        logging.info('sfhbs')
        self.d_DbHandler.connectToDb()
        cursor = self.d_DbHandler.getCursor()
        query = """
                SELECT DISTINCT *
                FROM dog_owners
                WHERE owner_email = '{0}'
                """.format(self.owner_email)
        logging.info(query)
        cursor.execute(query)
        info_lst = cursor.fetchone()
        self.owner_first_name = info_lst[1]
        self.owner_last_name =  info_lst[2]
        self.owner_phone = info_lst[3]
        self.dog_name = info_lst[4]
        self.dog_gender = info_lst[5]
        self.dog_type = info_lst[6]
        self.owner_city = info_lst[7]
        self.owner_full_name = "{0} {1}".format(self.owner_first_name, self.owner_last_name).title()

        cursor = self.d_DbHandler.getCursor()
        query = """
                SELECT t.day_of_week, w.first_name, w.last_name
                FROM trips as t join dog_walkers as w using (walker_email)
                WHERE t.owner_email ='{0}'
                """.format(self.owner_email)
        cursor.execute(query)
        info_lst = cursor.fetchall()
        for walker_info in info_lst:
            key = walker_info[0]
            cur_walker_name = "{0} {1}".format(walker_info[1], walker_info[2]).title()
            self.schedule[DAYS[key]] = self.schedule[DAYS[key]].append(cur_walker_name)

        logging.info('sfhbs')
        self.d_DbHandler.connectToDb()
        cursor = self.d_DbHandler.getCursor()
        query = """SELECT avg_hight, avg_weight FROM dog_types WHERE dog_type = '{0}'""".format(self.dog_type)
        cursor.execute(query)
        record = cursor.fetchone()
        if record is not None:
            self.dog_info['avg_height'] = record[0]
            self.dog_info['avg_weight'] = record[1]
        self.d_DbHandler.disconnectFromDb()
        logging.info('Finished insertion to DB!')


class Welcome():
    def __init__(self, email):
        self.email = email
        self.name = ""
        self.get_user_name()

    def get_user_name(self):
        logging.info('sfhbs')
        cursor = main.db_DbHandler.getCursor()
        query = """
                SELECT first_name,last_name
                FROM dog_owners
                WHERE owner_email = '{0}'
                """.format(self.email)
        cursor.execute(query)
        name = cursor.fetchone()
        if name != None:
            self.name = "{0} {1}".format(name[0],name[1]).title()
        main.db_DbHandler.disconnectFromDb()
        logging.info('Finished insertion to DB!')


class GeneralInfo:
    def __init__(self):
        # self.d_DbHandler = db_handler.DbHandler()
        self.cities = ''
        self.dog_types = ''
        self.get_info()

    def get_info(self):
        logging.info('sfhbs')
        # self.d_DbHandler.connectToDb()
        cursor = main.db_DbHandler.getCursor()
        query = """
                SELECT DISTINCT city_name
                FROM cities
                """
        main.db_DbHandler.connectToDb()
        cursor.execute(query)
        cities = cursor.fetchall()
        self.cities = [str(city[0]) for city in cities]
        main.db_DbHandler.disconnectFromDb()

        cursor = main.db_DbHandler.getCursor()
        query = """
                SELECT DISTINCT dog_type
                FROM walker_dog_types
                """
        cursor.execute(query)
        dog_types = cursor.fetchall()
        self.dog_types = [str(dog_type[0]) for dog_type in dog_types]
        main.db_DbHandler.disconnectFromDb()
        logging.info('Finished insertion to DB!')
