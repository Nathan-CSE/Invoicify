import os
import ssl, smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from os.path import basename
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate

load_dotenv()

def auth_request(email, code):
    '''
    Sends an email to the email requests if it exists within the database

    Arguments:
        email (string)      - A unique string which validates the user
        code (string)      - Unique code to reset password


    Return Value:
        Returns {} no matter what
    '''
    # if the email is valid, it allows it to be changed
        # users[user_index]["token"] = []
        # Sending the email
        # Create a secure SSL context

    context = ssl.create_default_context()
    sender_email = os.getenv("EMAIL_USER")
    sender_pass = os.getenv("EMAIL_PASS")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.ehlo()
        server.login(sender_email, sender_pass)
        text = f"""/
        Hi, you requested a password change,
        Reset code : {code}
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
    msg['Subject'] = "Tax Invoice"

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
        
def send_xml(send_to:list, text, file_name):
    '''
    Sends an email with an attachment

    Arguments:
        email (string)      - A unique string which validates the user
        text (string)       - UBL
        file_name (string)  - Attachment name


    Return Value:
        Returns 0 on success
        -1 on fail
    '''
    load_dotenv()
    context = ssl.create_default_context()
    sender_email = os.getenv("EMAIL_USER")
    sender_pass = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Tax Invoice"

    msg.attach(MIMEText(text))

    file_data = MIMEApplication(
        str.encode(text),
        Name=basename(file_name)
    )
    file_data['Content-Disposition'] = 'attachment; filename="%s"' % basename(file_name)
    msg.attach(file_data)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.ehlo()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, send_to, msg.as_string())
    return 0
if __name__ == "__main__":
    send_xml([""], "Hey Loser", "test")
