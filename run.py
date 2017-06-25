from flask import Flask, render_template, request;
from twilio.twiml.messaging_response import MessagingResponse;
from flask.ext.socketio import SocketIO, emit;

import sys;
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
        socketio.emit("removeTally", {});
    elif fromNumber in mainLottery.getWaitingUsers():
        msg = resp.message("Hey again {}-- you're currently registered for the next round, which will begin in {}. You can remove yourself from the round by texting \"REMOVE\" to this number.".format(fromNumber, mainLottery.getTimeLeft()));
    else:
        mainLottery.addWaitingUser(fromNumber);
        msg = resp.message("Thanks for the text, {}! You're now in the queue for the next round, which will begin in {}.".format(fromNumber, mainLottery.getTimeLeft()));
        socketio.emit("addTally", {});

    return str(resp);


@socketio.on("joined")
def joined(message):
    print("A user just accessed the site.");
    socketio.emit("setupTallies", {"numUsers": mainLottery.getNumberOfWaitingUsers()});
    # TODO: Organize events like these into a separate file
    # TODO: Emit event that sets up current number of people in the queue

if __name__ == "__main__":
    mainLottery = matcherTimer();
    #app.run(debug=True, use_reloader=False, host="0.0.0.0");
    socketio.run(app);
