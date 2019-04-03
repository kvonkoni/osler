import os,sys,math,csv
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis, CompareDiagnoses
from osler.issue import Issue
from osler.engine import Matrix

#Defining assertions

is_internet_connected = Assertion("Is connected to the internet", "Does the user have a stable internet connection?")
used_site_login = Assertion("Used site login page", "Has the user attempted to login from the site login?")
correct_email = Assertion("User entered the correct email address", "Does the Login Attempts report show the user's login attempt?")
incorrect_password = Assertion("User entered an incorrect password", "Does the Login Attempts report show an incorrect password?")
email_in_spam_folder = Assertion("Invitation/password reset email is in the user's spam/junk folder", "Is the invitation/password reset email in the user's email spam/junk folder?")
received_password_reset_email = Assertion("User received password reset email", "Did you receive a password reset email upon reset request?")

#Defining criteria

is_internet_connected_true = Criterion(is_internet_connected, True)
is_internet_connected_false = Criterion(is_internet_connected, False)
used_site_login_true = Criterion(used_site_login, True)
used_site_login_false = Criterion(used_site_login, False)
correct_email_true = Criterion(correct_email, True)
correct_email_false = Criterion(correct_email, False)
incorrect_password_true = Criterion(incorrect_password, True)
incorrect_password_false = Criterion(incorrect_password, False)
email_in_spam_folder_true = Criterion(received_password_reset_email, True)
email_in_spam_folder_false = Criterion(received_password_reset_email, False)
received_password_reset_email_true = Criterion(received_password_reset_email, True)
received_password_reset_email_false = Criterion(received_password_reset_email, False)

#Defining diagnoses

no_internet_connection = Diagnosis("User does not have an internet connection", "The user is not currently connected to the internet", "The user should find a stable internet connection.", {is_internet_connected_false}, 1)
no_attempt_reported = Diagnosis("No login attempt was recorded", "No login attempt was recorded since the user is using the global login", "Have the user use the site login page", {is_internet_connected_true, used_site_login_false}, 1000)
incorrect_email = Diagnosis("User entered incorrect email address", "The user entered an incorrect email address", "Encourage the user to discover the correct alternate email address and then confirm.", {is_internet_connected_true, used_site_login_true, is_internet_connected_true, correct_email_false}, 2000)
incorrect_password = Diagnosis("User entered incorrect password", "The user entered an incorrect password", "Send the user a password reset email link.", {is_internet_connected_true, used_site_login_true, correct_email_true, incorrect_password_true}, 100)
invalid_password = Diagnosis("User entered incorrect password", "The user entered an incorrect password", "Send the user a password reset email link.", {is_internet_connected_true, used_site_login_true, correct_email_true, incorrect_password_true, able_to_set_password_false}, 100)
email_filtered_as_spam = Diagnosis("User's invitation/password reset was filtered by their spam/junk folder", "The user's invitation/password reset was filtered by their spam/junk folder", "Put yourself as backup email, send new reset email, forward to user.", {is_internet_connected_true, email_in_spam_folder_true, received_password_reset_email_true, correct_email_true}, 10)
email_blocked_by_firewall = Diagnosis("User email blocked by firewall", "The user's company firewall is blocking emails from Firmex", "Send the user's company's IT department the whitelisting instructions.", {is_internet_connected_true, email_in_spam_folder_false, received_password_reset_email_false, correct_email_true}, 10)

#Defining an issue

CompareDiagnoses(incorrect_password, email_filtered_as_spam)

issue = Issue("Can't login: Invalid Credentials", "The user cannot login to their account. They are seeing an error that says invalid credentials.", {no_internet_connection, no_attempt_reported, incorrect_email, incorrect_password, email_filtered_as_spam, email_blocked_by_firewall})

#Building a test tree

matrix = Matrix(issue)
matrix.ConstructTree(True)

matrix.node.To_png("login_example.png")
