import os
import ssl, smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from os.path import basename
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from werkzeug.datastructures import FileStorage

load_dotenv()

def auth_request(email: str, code: str) -> dict:
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

def send_attachment(send_to: list[str], text: str, ubl_data: list[tuple[str, str]], files: list[FileStorage]) -> bool:
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
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.ehlo()
        server.login(sender_email, sender_pass)
        for ubl in ubl_data:
            file_data = MIMEApplication(
                str.encode(ubl[1]),
                Name=basename(ubl[0])
            )
            file_data['Content-Disposition'] = 'attachment; filename="%s"' % basename(ubl[0])
            msg.attach(file_data)
            try:
                server.sendmail(sender_email, send_to, msg.as_string())
            except:
                return False

        for f in files:
            file_data = MIMEApplication(
                f.read(),
                Name=f.filename
            )
            file_data['Content-Disposition'] = 'attachment; filename="%s"' % f.filename
            msg.attach(file_data)
            try:
                server.sendmail(sender_email, send_to, msg.as_string())
            except:
                return False
        
    return True
        
def send_xml(send_to: list[str], text: str, file_name: str):
    '''
    Sends an email with an attachment

    Arguments:
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
