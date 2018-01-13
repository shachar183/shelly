# -------------------------------------------------------------------------------
# Message Finder
# -------------------------------------------------------------------------------
# A class to find Messages in the DB
#-------------------------------------------------------------------------
# Author:	   Dan Avrahami
# Last updated: 08.12.2015
#-------------------------------------------------------------------------

# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
import MySQLdb

DAYS = {'Sunday':0, 'Monday':1, 'Tuesday':2, 'Wednesday':3,'Thursday':4 , 'Friday':5, 'Saturday':6}

class DogWalker():
    global DAYS
    def __init__(self,email_dogwalker, d_DbHandler):
        logging.info('Initializing MessageFinder')
        self.d_DbHandler = d_DbHandler
        self.dogwalker_email = email_dogwalker
        self.dogwalker_first_name = ""
        self.dogwalker_last_name =  ""
        self.dogwalker_full_name = ""
        self.dogwalker_phone = ""
        self.dogwalker_city = ""
        self.dogwalker_price= ""
        self.days_for_owner = [['Sunday', 'disabled'], ['Monday', 'disabled'] , ['Tuesday', 'disabled'], ['Wednesday', 'disabled'],
							   ['Thursday','disabled'] , ['Friday','disabled'], ['Saturday','disabled']]
        self.get_dogwalker_details()

    def get_dogwalker_details(self):
        logging.info('sfhbs')
        # self.d_DbHandler.connectToDb()
        cursor = self.d_DbHandler.getCursor()
        query = """
                SELECT first_name, last_name, phone_number, city_name, daily_rate 
                FROM dog_walkers
                WHERE walker_email = '{0}'
                """.format(self.dogwalker_email)
        cursor.execute(query)
        walker_info = cursor.fetchone()
        self.dogwalker_first_name = walker_info[0]
        self.dogwalker_last_name = walker_info[1]
        self.dogwalker_phone = walker_info[2]
        self.dogwalker_city = walker_info[3]
        self.dogwalker_price= walker_info[4]
        self.dogwalker_full_name = "{0} {1}".format(self.dogwalker_first_name,self.dogwalker_last_name).title()

        self.d_DbHandler.disconnectFromDb()
        logging.info('Finished insertion to DB!')

    def get_days_for_owner(self,owner_email):
        logging.info('sfhbs')
        self.d_DbHandler.connectToDb()
        cursor=self.d_DbHandler.getCursor()
        query = """
                SELECT DISTINCT(w.day_of_week)
				FROM working_days w JOIN prefered_walking_days p USING(day_of_week) 
					 LEFT OUTER JOIN (SELECT day_of_week 
									  FROM trips 
									  WHERE owner_email = '{0}' AND walker_email = '{1}') t
					ON (t.day_of_week = w.day_of_week)
				WHERE w.availability > 0 AND t.day_of_week IS NULL
					  AND p.owner_email = '{0}' AND w.walker_email = '{1}' 
                """.format(owner_email, self.dogwalker_email)
        cursor.execute(query)
        good_days = cursor.fetchall()
        logging.info("good days".format(good_days))
        for day in good_days:
            self.days_for_owner[DAYS[day[0]]][1] = 'enabled'
            logging.info("day".format(day))
        self.d_DbHandler.disconnectFromDb()
        logging.info('Finished insertion to DB!')

class DogWalkerFinder():
    def __init__(self,owner_email):
        logging.info('Initializing MessageFinder')
        self.d_DbHandler=db_handler.DbHandler()
        self.owner_email=owner_email
        # create data members of the class MessageFinder
        self.d_RetrievedDogWalkerList=[]

    def find_dog_walkers(self):
        logging.info('In MessageFinder.getAllMessages')
        self.d_DbHandler.connectToDb()
        cursor=self.d_DbHandler.getCursor()
        sql =	 """
					SELECT DISTINCT w.walker_email
					FROM dog_owners o JOIN prefered_walking_days p USING (owner_email) 
						 JOIN working_days w USING (day_of_week) JOIN walker_dog_types t USING (walker_email) 
						 JOIN dog_walkers d USING (walker_email)
					WHERE o.owner_email = '{0}' AND o.city_name = d.city_name
						  AND o.dog_type = t.dog_type
        			""".format(self.owner_email)
        cursor.execute(sql)
        dog_walker_emails = cursor.fetchall()
        self.d_DbHandler.disconnectFromDb()

        for email in dog_walker_emails:
            current_dogwalker = DogWalker(email[0], self.d_DbHandler)
            current_dogwalker.get_days_for_owner(self.owner_email)
            self.d_RetrievedDogWalkerList.append(current_dogwalker)



class NewTrip:

    def __init__(self, owner_email, walker_email, day):
        logging.info('Initializing MessageFinder')
        self.d_DbHandler = db_handler.DbHandler()
        self.owner_email = owner_email
        self.walker_email = walker_email
        self.day = day

    def insert_trip(self):
        logging.info('new trip')
        self.d_DbHandler.connectToDb()

        cursor=self.d_DbHandler.getCursor()
        query = """
                    INSERT INTO trips(walker_email, owner_email, day_of_week)
                    VALUES('{0}','{1}','{2}')
                    """.format(self.walker_email, self.owner_email, self.day)
        cursor.execute(query)
        self.d_DbHandler.commit()
        self.d_DbHandler.disconnectFromDb()

        cursor=self.d_DbHandler.getCursor()
        query = """
                UPDATE working_days
                SET availability = availability -1
                WHERE walker_email = '{0}' AND day_of_week = '{1}'
                """.format(self.walker_email, self.day)
        cursor.execute(query)
        self.d_DbHandler.commit()
        self.d_DbHandler.disconnectFromDb()
        logging.info('Finished insertion to DB!')