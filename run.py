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
    mainLottery.addUser("phonenumberplaceholder");
    msg = resp.message("Thanks for the text! You have been added to the lottery.");


    # Add a picture message
    #msg.media("https://farm8.staticflickr.com/7090/6941316406_80b4d6d50e_z_d.jpg")

    return str(resp);


if __name__ == "__main__":
    mainLottery = matcherTimer();
    app.run(debug=True, host="0.0.0.0");
