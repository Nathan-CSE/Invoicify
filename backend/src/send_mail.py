
from dotenv import load_dotenv
import ssl, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from os.path import basename
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
import os

def auth_request_v1(email):
    '''
    Sends an email to the email requests if it exists within the database

    Arguments:
        email (string)      - A unique string which validates the user

    Return Value:
        Returns {} no matter what
    '''
    
    email_found = False
    user_index = -1
    code = ""
    # if the email is valid, it allows it to be changed
    for user in users:
        if user["email"] == email:
            user_index = users.index(user)
            code = token_generator(user["auth_user_id"])
            user["code"].append(code)
            email_found = True

    if email_found:
        # users[user_index]["token"] = []
        # Sending the email
        # Create a secure SSL context
        load_dotenv()

        context = ssl.create_default_context()
        sender_email = os.getenv("EMAIL_USER")
        sender_pass = os.getenv("EMAIL_PASS")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.ehlo()
            server.login(sender_email, sender_pass)
            text = f"""/
            Hi, you requested a password change,
            Reset code : test
            """
            server.sendmail(sender_email, email, text)
    return {}

def send_attachment(send_to:list, text, files=None):
    '''
    Sends an email with an attachment

    Arguments:
        email (string)      - A unique string which validates the user


    Return Value:
        Returns {} no matter what
    '''
    load_dotenv()
    context = ssl.create_default_context()
    sender_email = os.getenv("EMAIL_USER")
    sender_pass = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Test"

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as file:
            file_data = MIMEApplication(
                file.read(),
                Name=basename(f)
            )
        file_data['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(file_data)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.ehlo()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, send_to, msg.as_string())

    return {}
        

# def auth_reset_v1(reset_code, password):
#     '''
#     Resets the users password when provided the correct reset code and password

#     Arguments:
#         reset_code (string) : a jwt token containing the users id
#         password (string)   : the changed password

#     Exceptions:
#         InputError  - Occurs when:
#                         - invalid token
#                         - password length is less the 6 characters

#     Return Value:
#         Returns {} when no error is raised
#     '''

#     if len(password) < 6:
#         raise InputError(description="password too short")
#     code_found = False
#     database = data_store.get()
#     users = database['users']
#     for user in users:
#         if reset_code in user['code']:
#             code_found = True
#             user['code'].remove(reset_code)
#             user["password"] = hasher(password)
#     if not code_found:
#         raise InputError(description="no code found")
#     return {}

if __name__ == "__main__":
    # auth_request_v1("")
    send_attachment([""], "Hey Loser", ["../test.txt"])
