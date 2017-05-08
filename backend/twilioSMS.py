from twilio.rest import Client;

tokenDict = {}; # Gets Twilio tokens from separate file
with open("tokens_DONOTPUSH.txt") as tokenfile:
    for line in tokenfile:
        (key, val) = line.split();
        tokenDict[key] = val;

ACCOUNT_SID = tokenDict["twilio_account_sid"];
AUTH_TOKEN  = tokenDict["twilio_auth_token"];
SENDER_NUMBER = tokenDict["twilio_sender_number"];

client = Client(ACCOUNT_SID, AUTH_TOKEN);

def sendSMS(recipientNumber, message):
    message = client.messages.create(
        to = recipientNumber,
        from_ = SENDER_NUMBER,
        body = message);
    print(message.sid);
    return;

sendSMS(tokenDict["my_number"], "test");
