from bottle import request, response, template
import sqlite3
import pathlib
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

##############################
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

##############################
def db():
    try:
        db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/database/email.db")
        db.execute("PRAGMA foreign_keys = ON")
        db.row_factory = dict_factory # JSON objects
        return db
    except Exception as ex:
        print("db function has an errror")
        print(ex)
    finally:
        pass

##############################
USER_NAME_MIN = 2
USER_NAME_MAX = 20
USER_NAME_REGEX = "^.{2,20}$"

def validate_user_name():
    error = f"user_name {USER_NAME_MIN} to {USER_NAME_MAX} characters"
    user_name = request.forms.get("user_name", "")
    user_name = user_name.strip()
    if not re.match(USER_NAME_REGEX, user_name): raise Exception(400, error)
    return user_name



##############################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
USER_LAST_NAME_REGEX = "^.{2,20}$"

def validate_user_last_name():
    error = f"user_last_name {USER_LAST_NAME_MIN} to {USER_LAST_NAME_MAX} characters"
    user_last_name = request.forms.get("user_last_name", "")
    user_last_name = user_last_name.strip()
    if not re.match(USER_LAST_NAME_REGEX, user_last_name): raise Exception(400, error)
    return user_last_name


##############################
USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_user_password():
    error = f"user_password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
    user_password = request.forms.get("user_password", "")
    user_password = user_password.strip()
    # if len(user_password) < USER_PASSWORD_MIN : raise Exception(400, error)
    # if len(user_password) > USER_PASSWORD_MAX : raise Exception(400, error)
    if not re.match(USER_PASSWORD_REGEX, user_password): raise Exception(400, error)
    return user_password


##############################

USER_EMAIL_MIN = 6
USER_EMAIL_MAX = 100
USER_EMAIL_REGEX = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

def validate_user_email():
	error = f"user_email invalid"
	user_email = request.forms.get("user_email", "")        
	user_email = user_email.strip()
	if len(user_email) < USER_EMAIL_MIN : raise Exception(400, error)
	if len(user_email) > USER_EMAIL_MAX : raise Exception(400, error)  
	if not re.match(USER_EMAIL_REGEX, user_email): raise Exception(400, error)
	return user_email

##############################
def disable_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)  

def send_email(user_name, receiver_email, verification_key):
    # Email configuration
    sender_email = "iffijarral@gmail.com"    
    password = "flolrybuytwclchl"
    subject = "Test Email via Python"
    # message_body = "<h1>Hello, this is a test email sent via Python!</h1>"
    message_body = template('email_welcome', user_name = user_name, verification_key = verification_key)
    # Create message container
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach message body
    message.attach(MIMEText(message_body, 'html'))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Quit SMTP session
        server.quit()

        return True
    except Exception as e:
        print("An error occurred:", e)
        return False
    finally:
        pass