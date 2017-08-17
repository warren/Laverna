import time, random, requests;
from threading import Timer;
from twilioSMS import *;
from flask.ext.socketio import SocketIO, emit;

TIMER_LENGTH = 30.0; # Time is measured in seconds
WARNING_TIMER_LENGTH = 25.0;

class matcherTimer():
    def __init__(self):
        self.waitingUsers = []; # Declares empty array of users waiting to be matched
        self.activeUsers = []; # Declares empty array of matched users
        self.activeUserPairs = [[]]; # Declares empty 2-d array of matched users

        self.timer = Timer(TIMER_LENGTH, self.pairUsers); # Prepares main threaded timer
        self.startTime = time.time(); # Sets start time so we can later check how long the timer has been running
        self.timer.start(); # Starts the threaded timer

        self.warningTimer = Timer(WARNING_TIMER_LENGTH, self.warnActiveUsers); # Prepares warning timer
        self.warningTimer.start();

        self.roundId = ("%064x" % (random.randrange(10**80)))[:64]; # Forgive me father for I have sinned; all you need to know is that this generates a random 64-digit hex string

        print("New matcher timer created for time {}.".format(TIMER_LENGTH));

    def resetTimer(self):
        self.timer = Timer(TIMER_LENGTH, self.pairUsers); # Sets start time to current time
        print("Matcher timer was just reset to length {}.".format(TIMER_LENGTH));
        requests.get("http://127.0.0.1:5000/tallyreset"); # Sends internal GET request that triggers the resetTallies socket emit. Hacky, but it seems necessary because flask_socketio won't allow importing SocketIO objects across modules
        self.startTime = time.time();
        self.timer.start();
        return;

    def resetRoundId(self):
        self.roundId = ("%064x" % (random.randrange(10**80)))[:64];
        return;

    def getRoundId(self):
        return self.roundId;

    def getTimeLeft(self):
        return TIMER_LENGTH - (time.time() - self.startTime); # Returns in seconds

    def getTimeLeftMessage(self):
        secondsLeft = self.getTimeLeft();
        hours, remainder = divmod(secondsLeft, 3600);
        minutes, seconds = divmod(remainder, 60);
        returnMessage = "";
        if int(hours) > 0:
            returnMessage += "{} hours, ".format(int(hours));
        if int(minutes) > 0:
            returnMessage += "{} minutes, ".format(int(minutes));
        returnMessage += "{} seconds".format(int(seconds));
        return returnMessage;

    def addWaitingUser(self, userNumber):
        self.waitingUsers.append(userNumber);
        print("User was just added to the matcher timer with phone number {}.".format(userNumber));
        return;

    def removeWaitingUser(self, userNumber):
        if userNumber in self.waitingUsers:
            self.waitingUsers.remove(userNumber);
            print("Successfully removed user from matcher with phone number {}.".format(userNumber));
            return;
        else:
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
        self.resetRoundId();
        return;

    def pairUsers(self):
        if self.getNumberOfWaitingUsers() <= 1: # If there aren't enough waitingUsers
            print("There were too few waiting users to start. Printing list of waitingUsers below:");
            print(self.getWaitingUsers());

            for iterUser in self.waitingUsers: # This should actually only send one message, since "too few" means <= 1 user
                sendSMS(iterUser, "Hey {}. Sorry, but there were too few players in the matching system ".format(iterUser) + \
                "to start a round! If you would like to be added to the next round though, just text this number again.");
            self.resetMatcherTimer();
            return;

        elif self.getNumberOfWaitingUsers() % 2 == 1: # If there are an odd number of waitingUsers
            aloneUser = self.getWaitingUsers[0]; # Picks one person to sit out
            self.removeWaitingUser(aloneUser);
            sendSMS(aloneUser, "Sorry! There was an odd " + \
            "number of players in the matching system! To pair everyone evenly you were chosen to sit out. " + \
            "If you would like to be added to the next round of matching, just text this number again.");
            # Sends message to the alone user saying they were chosen to sit out

        # We reach this point in the code if we have a good number of waitingUsers to start a round.
        for finishedUser in self.activeUsers:
            sendSMS(finishedUser, "Hey {}-- thanks for playing! The round is now over. To play again, text this number again!".format(finishedUser));

        random.shuffle(self.waitingUsers); # Scrambles the waitingUsers in the list
        self.activeUsers = self.waitingUsers;
        self.activeUserPairs = list(zip(*[iter(self.waitingUsers)]*2)); # Pairs the waitingUsers

        print("Users have been paired. Pairings as follows:");
        for firstUser, secondUser in self.activeUserPairs:
            sendSMS(firstUser, "Hey {}-- you are now paired with a random person. Say hi!".format(firstUser));
            sendSMS(secondUser, "Hey {}-- you are now paired with a random person. Say hi!".format(secondUser));
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

    def warnActiveUsers(self):
        for iterUser in self.activeUsers: # This should actually only send one message, since "too few" means <= 1 user
            sendSMS(iterUser, "Hey {}-- this round will be ending in {}. After that, you will be disconnected ".format(iterUser, self.getTimeLeftMessage()) + \
                            "from your match and this phone number will go back to registration mode.");
        return;
