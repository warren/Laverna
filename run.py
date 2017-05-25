from flask import Flask, render_template, request, redirect;
from twilio.twiml.messaging_response import MessagingResponse;

import sys;
sys.path.insert(0, "backend/"); # Allows importing from backend directory
from matcherTimer import *;
from twilioSMS import *;

app = Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/about")
def about():
    return render_template("about.html");

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    resp = MessagingResponse(); # Start our TwiML response

    fromNumber = request.values.get("From", None);

    if fromNumber in mainLottery.getActiveUsers():
        fromMessage = request.values.get("Body", None);
        sendSMS(mainLottery.getUserPairing(fromNumber), fromMessage);
    elif fromNumber in mainLottery.getWaitingUsers():
        msg = resp.message("Hey again {}-- you're currently registered for the next round, which will begin in placeholder years.".format(fromNumber));
        # TODO: Tell user when round will start
        # TODO: Implement a way for users to deadd themselves from the queue
    else:
        mainLottery.addWaitingUser(fromNumber);
        msg = resp.message("Thanks for the text, {}! You're now in the queue for the next round.".format(fromNumber));
        # TODO: Tell user when round will start

    return str(resp);


if __name__ == "__main__":
    mainLottery = matcherTimer();
    app.run(debug=True, use_reloader=False, host="0.0.0.0");
