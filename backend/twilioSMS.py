from twilio.rest import Client;
import re; # Import regex

tokenDict = {}; # Gets Twilio tokens from separate file
with open("backend/tokens_DONOTPUSH.txt") as tokenFile: # Path starts at backend/ because this module being run from run.py
    for line in tokenFile:
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

def getMagicNumber():
    return tokenDict["twilio_sender_number"];

def checkUniqueUser(fromNumber):
    fromNumber = re.sub(r'[^\w]', '', fromNumber); # Removes all non-alphanumeric and non-underscore characters

    hashedNumber = 0; # TODO: SHA256 goes here
    with open("backend/uniquehashes.txt") as hashesFile:
        for line in hashesFile:
            if line == hashedNumber:
                return False;
        hashesFile.write(hashedNumber + "\n");
        return True;
