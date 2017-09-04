from flask import Flask, render_template, request;
from twilio.twiml.messaging_response import MessagingResponse;
from flask.ext.socketio import SocketIO, emit;

import sys, random;
sys.path.insert(0, "backend/"); # Allows importing from backend directory
from matcherTimer import *;
from twilioSMS import *;

app = Flask(__name__);
socketio = SocketIO(app);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/about")
def about():
    return render_template("about.html");

@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    # TODO...?: Allow users to send pictures
    resp = MessagingResponse(); # Start our TwiML response

    fromNumber = request.values.get("From", None); # This is our sender's phone number
    fromMessage = request.values.get("Body", None); # This is the message our sender sent

    # If the user is playing in the round:
    if fromNumber in mainLottery.getActiveUsers():
        sendSMS(mainLottery.getUserPairing(fromNumber), fromMessage); # Routes the sender's message to their pair and does not text back the sender

    # If the user is removing themselves from the queue:
    elif fromNumber in mainLottery.getWaitingUsers() and fromMessage == "REMOVE":
        mainLottery.removeWaitingUser(fromNumber);
        msg = resp.message("{}: You have been removed from the waiting queue.".format(mainLottery.getUserId(fromNumber)));
        iconName = tallyIconDict.pop(fromNumber);
        # TODO: Fix potential valueError bug when unqueued user texts "REMOVE"
        socketio.emit("removeTally", {"iconName": iconName});

    # If the user is registered for the next round and is texting again:
    elif fromNumber in mainLottery.getWaitingUsers():
        msg = resp.message("{}: The round has not started yet. If you want to exit the waiting queue, text \"REMOVE\" to this number".format(mainLottery.getUserId(fromNumber)));

    # If the user is has not been added to the queue yet:
    else:
        if checkUniqueUser(fromNumber) == True:
            print("A unique user just texted the number.");
            socketio.emit("setUniqueUsers", getUniqueUserCount());

        mainLottery.addWaitingUser(fromNumber);
        msg = resp.message("You are now queued for the next round, which begins in {} seconds. Your unique identifier is {}; any message not containing this code was sent by another person.".format(mainLottery.getTimeLeft(), mainLottery.getUserId(fromNumber)));
        iconName = random.choice(open("iconlist.txt").readlines());
        while iconName in tallyIconDict: # If we have picked an icon that is already in use...
            iconName = random.choice(open("iconlist.txt").readlines()); # ... pick another and check again.
        tallyIconDict[fromNumber] = iconName;
        socketio.emit("addTally", {"iconName": iconName});

    return str(resp);

@app.route("/tallyreset")
def tallyreset():
    socketio.emit("resetTallies");
    return "/tallyreset endpoint says 200!";

@socketio.on("joined")
def joined(message):
    print("Socket 'joined' was just called.");
    iconNamesToAdd = [];
    if bool(tallyIconDict): # If our dictionary is not empty
        for key, value in tallyIconDict.items():
            iconNamesToAdd.append(value); # Append all icon names

    socketio.emit("setup", {"iconList": iconNamesToAdd, "seconds": mainLottery.getTimeLeft(), "magicNumber": getMagicNumber(), "uniqueUsers": getUniqueUserCount()});


if __name__ == "__main__":
    mainLottery = matcherTimer();
    tallyIconDict = {};
    #app.run(debug=True, use_reloader=False, host="0.0.0.0");
    socketio.run(app);
