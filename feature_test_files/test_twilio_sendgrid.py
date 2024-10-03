# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from insuradmin_backend.settings import SENDGRID_API_KEY

message = Mail(
    from_email='service@duewiger.com',
    to_emails='kd@duewiger.com',
    subject='Ihr Kunde',
    html_content='<strong>Bitte kündigen Sie meine Haftpflichtversicherung.</strong>')
try:
    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)