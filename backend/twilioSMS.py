from twilio.rest import Client;
import re; # Import regex
import hashlib;

tokenDict = {}; # Gets Twilio tokens from separate file
with open("backend/tokens_DONOTPUSH.txt") as tokenFile: # Path starts at backend/ because this module being run from run.py
    for line in tokenFile:
        (key, val) = line.split();
        tokenDict[key] = val;

ACCOUNT_SID = tokenDict["twilio_account_sid"];
AUTH_TOKEN  = tokenDict["twilio_auth_token"];
SENDER_NUMBER = tokenDict["twilio_sender_number"];

uniqueUserCount = 0;
with open("backend/uniquehashes.txt") as setupHashesFile:
    for line in setupHashesFile:
        global uniqueUserCount;
        uniqueUserCount = uniqueUserCount + 1; # TODO: There must be a more efficient way of doing this


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
    hashedNumber = computeHash(fromNumber);

    with open("backend/uniquehashes.txt", "r+") as hashesFile:
        for line in hashesFile:
            if line.rstrip("\n") == hashedNumber:
                return False;
        hashesFile.write(hashedNumber + "\n");
        global uniqueUserCount
        uniqueUserCount = uniqueUserCount + 1;
        return True;

def computeHash(phoneNumber):
    phoneNumber = re.sub(r'[^\w]', '', phoneNumber); # Removes all non-alphanumeric and non-underscore characters
    phoneNumber = phoneNumber.encode("utf-8") # Encoding needed for hashing

    return hashlib.sha256(phoneNumber).hexdigest();

def getUniqueUserCount():
    global uniqueUserCount;
    return uniqueUserCount;
