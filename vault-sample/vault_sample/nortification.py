import os
import smtplib
from email.mime.text import MIMEText
from typing import List


def send_email(
    subject: str,
    body: str,
    sender: str,
    recipients: List[str],
) -> None:
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, os.environ["GMAIL_PASSWORD"])
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

    return None
