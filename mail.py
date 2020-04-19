import base64
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, Content, Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")


def send_certificate(name: str, email_address: str, cert: str, credential_id: str):
    with open('../bov-cert/bov-email.html', 'r') as email:
        message = (
            email.read()
            .replace("{name}", name)
            .replace("{credential_id}", credential_id)
        )
    content = Content("text/html", message)
    subject = "Battle of Vars 2020 Certificate"
    from_email = ("noreply@thescriptgroup.in", "TSG Bot")
    to_email = (email_address, name)
    mail = Mail(from_email, to_email, subject, html_content=content)
    mail.add_cc(("battleofvars@thescriptgroup.in", "Battle of Vars"))
    with open(cert, "rb") as img:
        img_data = img.read()
    encoded = base64.b64encode(img_data).decode()
    mail.add_attachment(Attachment(encoded, "certificate.jpg", "image/png"))

    try:
        response = SendGridAPIClient(SENDGRID_API_KEY).send(mail)
        print(f"Sent {cert} to {name} at {email_address}, id {credential_id}")
    except Exception as e:
        print(e)
        print(e.body)
