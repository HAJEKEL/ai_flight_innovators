from decouple import config
from twilio.rest import Client

account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
twilio_phone_number = config("TWILIO_PHONE_NUMBER")
my_phone_number = config("MY_PHONE_NUMBER")
print(my_phone_number)
print(twilio_phone_number)
client = Client(account_sid, auth_token)

try:
    call = client.calls.create(
        to=my_phone_number,
        from_=twilio_phone_number,  # Use your Twilio phone number here
        url="http://demo.twilio.com/docs/voice.xml"
    )
    print(f"Call SID: {call.sid}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
