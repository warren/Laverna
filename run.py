from flask import Flask, render_template, request, redirect;
from twilio.twiml.messaging_response import MessagingResponse;

import sys;
sys.path.insert(0, "backend/"); # Allows importing from backend directory
from matcherTimer import *;

app = Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/about")
def about():
    return render_template("about.html");

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a text message
    fromNumber = request.values.get("From", None);
    listOfUsers = mainLottery.getListOfUsers();
    if fromNumber in listOfUsers:
        msg = resp.message("Thanks for the text, {}, but you are already in the lottery!".format(fromNumber));
    else:
        mainLottery.addUser(fromNumber);
        msg = resp.message("Thanks for the text, {}! You have been added to the lottery.".format(fromNumber));

    return str(resp);


if __name__ == "__main__":
    mainLottery = matcherTimer();
    # This creates a duplicate MT because the server restarts on startup
    app.run(debug=True, host="0.0.0.0");
