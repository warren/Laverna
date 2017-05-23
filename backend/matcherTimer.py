import time, random;
from threading import Timer;
from twilioSMS import *;
from smsConnector import *;

TIMER_LENGTH = 30.0; # Time is measured in seconds

class matcherTimer():
    def __init__(self):
        self.users = []; # Declares empty array of users in the matcher

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

    def addUser(self, userNumber):
        self.users.append(userNumber);
        print("User was just added to the matcher timer with phone number {}.".format(userNumber));
        return;

    def removeUser(self, userNumber):
        for i in self.users:
            if self.users[i] == userNumber:
                # TODO: self.users.remove(INDEX OF i)
                print("Successfully removed user from matcher with phone number {}.".format(userNumber));
                return;

        print("ERROR: Tried to remove a user from the matcher who was not present in the matcher, with" + \
        "phone number {}.".format(userNumber));
        return;

    def getListOfUsers(self):
        return self.users;

    def getNumberOfUsers(self):
        return len(self.users);

    def resetMatcherTimer(self):
        self.users = [];
        self.resetTimer();
        return;

    def pairUsers(self):
        if self.getNumberOfUsers() <= 1: # If there aren't enough users
            print("There were too few users in the lottery to start. Printing list of users below:");
            print(self.getListOfUsers);

            for iterUser in self.users: # This should actually only send one message, since "too few" means <= 1 user
                sendSMS(iterUser, "Sorry about this, but there were too few users in the matching system " + \
                "to start a round! If you would like to be added to the next round though, just text this number again.");
            self.resetMatcherTimer();
            return;

        elif self.getNumberOfUsers() % 2 == 1: # If there are an odd number of users
            aloneUserNumber = self.getListOfUsers[0]; # Picks one person to sit out
            self.removeUser(aloneUserNumber);
            sendSMS(aloneUserNumber, "Sorry about this, but there was an odd " + \
            "number of users in the matching system! You were chosen to sit out. " + \
            "If you would like to be added to the next round of matching, just text this number again.");
            # Sends message to the alone user saying they were chosen to sit out

        # We reach this point in the code if we have a good number of users to start a round.
        random.shuffle(self.users); # Scrambles the users in the list
        userPairs = list(zip(*[iter(self.users)]*2)); # Pairs the users
        print("Users have been paired. Pairings as follows:");
        for firstUser, secondUser in userPairs:
            print("{} and {}".format(firstUser, secondUser));

        # del mainConnector; # TODO: Test if this is necessary
        mainConnector = smsConnector(self.users, userPairs);

        self.resetMatcherTimer(); # Resets the timer to do this all over again

        return;
