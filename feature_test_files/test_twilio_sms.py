# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

from insuradmin_backend.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFICATION_SERVICE_SID, TWILIO_CALLER_ID

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

verification = client.verify \
                     .v2 \
                     .services(TWILIO_VERIFICATION_SERVICE_SID) \
                     .verifications \
                     .create(to=TWILIO_CALLER_ID, channel='sms')

print(verification.sid)