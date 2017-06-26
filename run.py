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

    if fromNumber in mainLottery.getActiveUsers():
        sendSMS(mainLottery.getUserPairing(fromNumber), fromMessage);
    elif fromNumber in mainLottery.getWaitingUsers() and fromMessage == "REMOVE":
        mainLottery.removeWaitingUser(fromNumber);
        msg = resp.message("You have been successfully removed from the waiting queue for the next round. Rejoin at any time by texting this number again.");
        iconName = tallyIconDict.pop(fromNumber);
        # TODO: Fix potential valueError bug when unqueued user texts "REMOVE"
        socketio.emit("removeTally", {"iconName": iconName});
    elif fromNumber in mainLottery.getWaitingUsers():
        msg = resp.message("Hey again {}-- you're currently registered for the next round, which will begin in {}. You can remove yourself from the round by texting \"REMOVE\" to this number.".format(fromNumber, mainLottery.getTimeLeft()));
    else:
        mainLottery.addWaitingUser(fromNumber);
        msg = resp.message("Thanks for the text, {}! You're now in the queue for the next round, which will begin in {}.".format(fromNumber, mainLottery.getTimeLeft()));
        # TODO: Address user by their icon instead of their phone number
        iconName = random.choice(open("iconlist.txt").readlines());
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
    if bool(tallyIconDict): # If our dictionary is not empty
        iconNamesToAdd = [];
        for key, value in tallyIconDict.items():
            iconNamesToAdd.append(value); # Append all icon names

        socketio.emit("setupTallies", {"iconList": iconNamesToAdd});


if __name__ == "__main__":
    mainLottery = matcherTimer();
    tallyIconDict = {};
    #app.run(debug=True, use_reloader=False, host="0.0.0.0");
    socketio.run(app);
