import time;
from threading import Timer;

class matcherTimer():
    def __init__(self):
        self.users = []; # Array of users in the matcher

        self.timer = Timer(60.0, self.pairUsers); # Prepares threaded timer
        self.startTime = time.time(); # Sets start time so we can later check how long the timer has been running
        self.timer.start(); # Starts the threaded timer

        print("New matcher timer created.");

    def resetTimer(self):
        self.timer = Timer(5.0, self.pairUsers); # Sets start time to current time
        return;

    def getTimerUptime(self):
        return time.time() - self.startTime;

    def getTimeLeft(self):
        return (60*60) - self.getTimerUptime();
        # Time left out of an hour: 60 seconds * 60 minutes

    def addUser(self, userNumber):
        self.users.append(userNumber);
        print("User was just added to the matcher timer with phone number " + str(userNumber));
        return;

    def removeUser(self, userNumber):
        #TODO Make this remove a user from the matcher by phone number
        return;

    def getListOfUsers(self):
        return self.users;

    def getNumberOfUsers(self):
        return len(self.users);

    def pairUsers(self):
        if self.getNumberOfUsers() <= 1: # If there aren't enough users
            print("There were too few users in the lottery to start.");
            print(self.getListOfUsers);
            return;
        elif self.getNumberOfUsers() % 2 == 1: # If there are an odd number of users
            aloneUserNumber = self.getListOfUsers[0]; # Picks one person to sit out
            self.removeUser(aloneUserNumber);
            #TODO: Send message to the alone user saying they were chosen to sit out

        random.shuffle(self.users);
        userPairs = zip(*[iter(self.users)]*2);
        print("Users have been paired. Pairings as follows:")

        for firstUser, secondUser in userPairs:
            print(str(firstUser), "and", str(secondUser));

        return;
