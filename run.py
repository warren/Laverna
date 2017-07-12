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
        sendSMS(mainLottery.getUserPairing(fromNumber), fromMessage);

    # If the user is removing themselves from the queue:
    elif fromNumber in mainLottery.getWaitingUsers() and fromMessage == "REMOVE":
        mainLottery.removeWaitingUser(fromNumber);
        msg = resp.message("You have been successfully removed from the waiting queue for the next round. Rejoin at any time by texting this number again.");
        iconName = tallyIconDict.pop(fromNumber);
        # TODO: Fix potential valueError bug when unqueued user texts "REMOVE"
        socketio.emit("removeTally", {"iconName": iconName});

    # If the user is registered for the next round and is texting again:
    elif fromNumber in mainLottery.getWaitingUsers():
        msg = resp.message("Hey again {}-- you're currently registered for the next round, which will begin in {}. You can remove yourself from the round by texting \"REMOVE\" to this number.".format(fromNumber, mainLottery.getTimeLeft()));

    # If the user is has not been added to the queue yet:
    else:
        mainLottery.addWaitingUser(fromNumber);
        msg = resp.message("Thanks for the text, {}! You're now in the queue for the next round, which will begin in {}.".format(fromNumber, mainLottery.getTimeLeft()));
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
    print("A user just accessed the site.");
    iconNamesToAdd = [];
    if bool(tallyIconDict): # If our dictionary is not empty
        for key, value in tallyIconDict.items():
            iconNamesToAdd.append(value); # Append all icon names

    socketio.emit("setup", {"iconList": iconNamesToAdd, "seconds": mainLottery.getTimeLeft(), "magicNumber": "(123) 456-7890"});


if __name__ == "__main__":
    mainLottery = matcherTimer();
    tallyIconDict = {};
    #app.run(debug=True, use_reloader=False, host="0.0.0.0");
    socketio.run(app);
