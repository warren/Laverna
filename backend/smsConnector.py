from twilioSMS import *; # TODO: Test if this is necessary

class smsConnector():
    def __init__(self, users, userPairs):
        self.users = users;
        self.userPairs = userPairs;

    def containsUserNumber(self, userNumber):
        if userNumber in self.users:
            return True;
        else:
            return False;

    def getUserPairing(self, userNumber):
        if self.containsUserNumber(userNumber):
            for i in range(userPairs): # Search in userPairs to find pairing
                if findthisdude in userPairs[i]:
                    if findthisdude == userPairs[i][0]:
                        return userPairs[i][1];
                    else:
                        return userPairs[i][0];
        else:
            return "NO PAIRING";
