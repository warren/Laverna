from flask import Flask, render_template, request, redirect;
from twilio.twiml.messaging_response import MessagingResponse;

import sys;
sys.path.insert(0, "backend/"); # Allows importing from backend directory
from matcherTimer import *;
from smsConnector import *;

app = Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/about")
def about():
    return render_template("about.html");

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    resp = MessagingResponse() # Start our TwiML response

    fromNumber = request.values.get("From", None); # Add a text message

    if fromNumber in mainConnector.getUsers():
        # TODO: Reroute message to the appropriate paired user
        print("{} is in the group of active users, and is paired with {}".format(fromNumber, mainConnector.getUserPairing(fromNumber)));
    elif fromNumber in mainLottery.getListOfUsers():
        msg = resp.message("Thanks for the text, {}, but you are already in the lottery!".format(fromNumber));
        # TODO: Implement a way for users to deadd themselves from the queue
    else:
        mainLottery.addUser(fromNumber);
        msg = resp.message("Thanks for the text, {}! You have been added to the lottery.".format(fromNumber));

    return str(resp);


if __name__ == "__main__":
    mainLottery = matcherTimer();
    mainConnector = smsConnector([], []);
    app.run(debug=True, use_reloader=False, host="0.0.0.0");
