# ------------------------------------------------------
# Send Mail with Database
# ------------------------------------------------------
# The application demonstrates how to create a new message 
# form and submit it.
# The post method will handle the submitted message: 
# 1. Display the arrived message.
# 2. Store the message in the database
# The application will also allow to show all the messages in the DB.
# ------------------------------------------------------
# Author	   - Dan Avrahami
# Last updated - 2015-12-21								
# ------------------------------------------------------

import webapp2
import jinja2
import os
import logging
from google.appengine.api import users
# import the class message
import owner_details
# import the class dog_walker_finder
import dog_walker_finder
import db_handler

jinja_environment = jinja2.Environment(loader=
                                       jinja2.FileSystemLoader(os.path.dirname(__file__)))

db_DbHandler = db_handler.DbHandler()
# -------------------------------------------------------------
# class to create the form of the new message
# and submit it (by clicking Send)
# -------------------------------------------------------------

class Register(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "New Message" form
    def get(self):
        # Display the form
        user = users.get_current_user()
        email = user.email()
        dog_owner = owner_details.Welcome(email)
        if dog_owner.name != "":
            self.redirect('/welcome_back')
        info_register = owner_details.GeneralInfo()
        # send email to shelly
        # Display the message
        # ----------------------------------------------
        # the template will use a show_message.html file
        template = jinja_environment.get_template('user_login.html')
        # define the parameters and their name
        # that we will send to the template
        parameters_for_template = {'owner_email': email, 'info_register': info_register}
        self.response.write(template.render(parameters_for_template))


# -------------------------------------------------------------
# class to create the form of the new message
# and submit it (by clicking Send)
# -------------------------------------------------------------
class Welcome_back(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "New Message" form
    def get(self):
        user = users.get_current_user()
        email = user.email()
        dog_owner = owner_details.Welcome(email)
        if dog_owner.name == "":
            self.redirect('/')
        # Display the form
        template = jinja_environment.get_template('welcome_back.html')
        # define the parameters and their name
        # that we will send to the template
        parameters_for_template = {'owner_name': dog_owner.name}
        self.response.write(template.render(parameters_for_template))


class Welcome(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "New Message" form
    def post(self):
        user = users.get_current_user()
        dog_owner = owner_details.Account(user.email())

        # Request data from the POST request
        dog_owner.owner_first_name = self.request.get('owner_first_name')
        dog_owner.owner_last_name = self.request.get('owner_last_name')
        dog_owner.owner_phone = self.request.get('owner_phone')
        dog_owner.dog_name = self.request.get('dog_name')
        dog_owner.dog_gender = self.request.get('dog_gender')
        dog_owner.dog_type = self.request.get('dog_type')
        dog_owner.owner_city = self.request.get('owner_city')
        dog_owner.prefered_walking_days = self.request.get('day', allow_multiple=True)

        dog_owner.insert_owner_detail()

        email = user.email()
        dog_owner = owner_details.Welcome(email)
        template = jinja_environment.get_template('welcome.html')
        # define the parameters and their name
        # that we will send to the template
        parameters_for_template = {'owner_name': dog_owner.name}
        self.response.write(template.render(parameters_for_template))
        # ----------------------------------------
        # Add the Message into the database
        # ----------------------------------------
        # ----------------------------------------------

    def get(self):
        user = users.get_current_user()
        email = user.email()
        dog_owner = owner_details.Welcome(email)
        if dog_owner.name == "":
            self.redirect('/')
        # Display the form
        template = jinja_environment.get_template('welcome.html')
        # define the parameters and their name
        # that we will send to the template
        parameters_for_template = {'owner_name': dog_owner.name}
        self.response.write(template.render(parameters_for_template))


class Account(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        email = user.email()
        dog_owner = owner_details.Welcome(email)
        if dog_owner.name == "":
            self.redirect('/')
        current_owner = owner_details.Account(email)
        current_owner.get_owner_detail()
        # ----------------------------------------------
        # Display the message
        # ----------------------------------------------
        # the template will use a show_message.html file
        template = jinja_environment.get_template('account.html')

        # define the parameters and their name
        # that we will send to the template
        parameters_for_template = {'current_owner': current_owner}
        self.response.write(template.render(parameters_for_template))


class ChooseDogWalker(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        email = user.email()
        dog_owner = owner_details.Welcome(email)
        if dog_owner.name == "":
            self.redirect('/')
        dog_walkers = dog_walker_finder.DogWalkerFinder(email)
        dog_walkers.find_dog_walkers()
        retrieved_dog_walkers = dog_walkers.d_RetrievedDogWalkerList
        # Display the messages using jinja2
        parameters_for_template = {'list_of_dogwalkers': retrieved_dog_walkers, 'dog_owner': dog_owner}
        my_template = jinja_environment.get_template('dog_walkers.html')
        self.response.out.write(my_template.render(parameters_for_template))

class Logout(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "New Message" form
    def get(self):
        self.redirect(users.create_logout_url('/'))

class WalkerInfo(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "New Message" form
    def post(self):
        user = users.get_current_user()
        logging.info("here")
        trips_from_html = self.request.get('trip', allow_multiple=True)
        print "jere"

        # class Thankyou(webapp2.RequestHandler):
        #     # When we receive an HTTP POST request - display the "New Message" form
        #     def get(self):
        #     #     print "herer"
        #     #     user = users.get_current_user()

#     #     # logging.info(trips_from_html)
#     #     # for trip in trips_from_html:
#     #     #     new_trip = dog_walker_finder.NewTrip(user.email(), trip[0], trip[1])
#     #     #     new_trip.insert_trip()
#         print "here"
#         pass


# -------------------------------------------------------------
# Routing
# -------------------------------------------------------------
app = webapp2.WSGIApplication([('/welcome_back', Welcome_back),
                               ('/welcome', Welcome),
                               ('/account', Account),
                               ('/logout', Logout),
                               ('/dogwalker', ChooseDogWalker),
                               ('/walkerinfo', WalkerInfo),
                               ('/', Register)],
                              debug=False)
