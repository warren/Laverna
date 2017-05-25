import time, random;
from threading import Timer;
from twilioSMS import *;

TIMER_LENGTH = 30.0; # Time is measured in seconds

class matcherTimer():
    def __init__(self):
        self.waitingUsers = []; # Declares empty array of users waiting to be matched
        self.activeUsers = []; # Declares empty array of matched users
        self.activeUserPairs = [[]]; # Declares empty 2-d array of matched users

        # TODO: Start another timer to send users a warning when the pairings will shuffle

        self.timer = Timer(TIMER_LENGTH, self.pairUsers); # Prepares threaded timer
        self.startTime = time.time(); # Sets start time so we can later check how long the timer has been running
        self.timer.start(); # Starts the threaded timer

        print("New matcher timer created for time {}.".format(TIMER_LENGTH));

    def resetTimer(self):
        self.timer = Timer(TIMER_LENGTH, self.pairUsers); # Sets start time to current time
        print("Matcher timer was just reset to length {}.".format(TIMER_LENGTH));
        self.startTime = time.time();
        self.timer.start();
        return;

    def getTimerUptime(self):
        return time.time() - self.startTime;

    def getTimeLeft(self):
        return TIMER_LENGTH - self.getTimerUptime();

    def addWaitingUser(self, userNumber):
        self.waitingUsers.append(userNumber);
        print("User was just added to the matcher timer with phone number {}.".format(userNumber));
        return;

    def removeWaitingUser(self, userNumber):
        for i in self.waitingUsers:
            if self.waitingUsers[i] == userNumber:
                # TODO: self.waitingUsers.remove(INDEX OF i)
                print("Successfully removed user from matcher with phone number {}.".format(userNumber));
                return;

        print("ERROR: Tried to remove a user from the matcher who was not present in the matcher, with" + \
        "phone number {}.".format(userNumber));
        return;

    def getWaitingUsers(self):
        return self.waitingUsers;

    def getNumberOfWaitingUsers(self):
        return len(self.waitingUsers);

    def resetMatcherTimer(self):
        self.waitingUsers = [];
        self.resetTimer();
        return;

    def pairUsers(self):
        if self.getNumberOfWaitingUsers() <= 1: # If there aren't enough waitingUsers
            print("There were too few waitingUsers in the lottery to start. Printing list of waitingUsers below:");
            print(self.getWaitingUsers);

            for iterUser in self.waitingUsers: # This should actually only send one message, since "too few" means <= 1 user
                sendSMS(iterUser, "Sorry about this, but there were too few waitingUsers in the matching system " + \
                "to start a round! If you would like to be added to the next round though, just text this number again.");
            self.resetMatcherTimer();
            return;

        elif self.getNumberOfWaitingUsers() % 2 == 1: # If there are an odd number of waitingUsers
            aloneUserNumber = self.getWaitingUsers[0]; # Picks one person to sit out
            self.removeWaitingUser(aloneUserNumber);
            sendSMS(aloneUserNumber, "Sorry about this, but there was an odd " + \
            "number of waitingUsers in the matching system! You were chosen to sit out. " + \
            "If you would like to be added to the next round of matching, just text this number again.");
            # Sends message to the alone user saying they were chosen to sit out

        # We reach this point in the code if we have a good number of waitingUsers to start a round.
        random.shuffle(self.waitingUsers); # Scrambles the waitingUsers in the list
        self.activeUsers = self.waitingUsers;
        self.activeUserPairs = list(zip(*[iter(self.waitingUsers)]*2)); # Pairs the waitingUsers

        print("Users have been paired. Pairings as follows:");
        for firstUser, secondUser in self.activeUserPairs:
            print("{} and {}".format(firstUser, secondUser));

        self.resetMatcherTimer(); # Resets the timer to do this all over again

        return;

    # This is where I combined the matcherTimer and smsConnector files. The following methods
    # pertain to the matched users:

    def getActiveUsers(self):
        return self.activeUsers;

    def containsUserNumber(self, userNumber):
        if userNumber in self.activeUsers:
            return True;
        else:
            return False;

    def getUserPairing(self, userNumber):
        if self.containsUserNumber(userNumber):
            for i in range(len(self.activeUserPairs)): # Search in activeUserPairs to find pairing
                if userNumber in self.activeUserPairs[i]:
                    if userNumber == self.activeUserPairs[i][0]:
                        return self.activeUserPairs[i][1];
                    else:
                        return self.activeUserPairs[i][0];
        else:
            return "NO PAIRING";
