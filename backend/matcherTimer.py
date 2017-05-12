import time;
from threading import Timer;

class matcherTimer():
    def __init__(self):
        self.users = []; # Array of users in the matcher

        self.timer = Timer(5.0, self.pairUsers); # Prepares threaded timer
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

    def getNumberOfUsers(self):
        return len(users);

    def pairUsers(self):
        # TODO
        return;
