$(document).ready(function()
{
    var socket = io.connect("http://" + document.domain + ":" + location.port);
    socket.on("connect", function()
    {
        socket.emit("joined", {});
        console.log("A user just accessed the site.");
    });

    socket.on("addTally", function(data)
    {
        $("#tallyIcons").append('<i class="fa ' + data.iconName + '"></i>');
        // data.iconName is a string containing the name of the chosen fa-icon
        console.log("Tally added!");
        // TODO: Make this update #user-count-subtext
    });

    socket.on("removeTally", function(data)
    {
        $("i:." + data.iconName, "#tallyIcons").remove();
        // Removes all i elements of tallyIcons that have the class name iconName
        console.log("Tally with id " + data.iconName + "removed!");
        // TODO: Make this update #user-count-subtext
    });

    socket.on("setup", function(data)
    {
        setupTallies(data.iconList);
        setupTimer(data.seconds);
        console.log("Time left is " + Math.floor(data.seconds));
        setupPhoneNumber(data.magicNumber);
        console.log("Magic number is " + data.magicNumber);
    });

    socket.on("resetTallies", function()
    {
        $("#tallyIcons").empty();
        console.log("Tallies reset!");
    });
});

function setupTallies(iconList)
{
    for(i=0; i<iconList.length; i++)
    {
        $("#tallyIcons").append('<i class="fa ' + iconList[i] + '"></i>');
    };
    $("#user-count-subtext").text("There are currently " + iconList.length + " users in the queue.");
    // TODO: Make this write the correct string: "no users"/"user"/"users"
    // Maybe in helper method
    console.log("Tallies set up!");
}

function setupTimer(secondsLeft)
{
    var nowDate = new Date().getTime();
    // This is the # of milliseconds since Jan 1 1970 00:00:00
    var countdownDate = new Date(nowDate + (secondsLeft * 1000)).getTime();
    // This constructs a countdown date ahead of our current time by (secondsLeft * 100) milliseconds

    var x = setInterval(function()
    {
        var nowDate = new Date().getTime();
        var distance = countdownDate - nowDate;

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        $("#timer-subtext").text("and the next round will begin in " + hours + " hours, " + minutes + " minutes, and " + seconds + " seconds.");
    });
    // TODO: Make this timer reset itself with secondsLeft when it reaches 0
}

function setupPhoneNumber(magicNumber)
{
    magicNumber = magicNumber.replace(/[^\d]/g, "");
    // Removes all characters that aren't 0-9 from the string
    magicNumber = magicNumber.substr(1);
    // Removes the first character, which will be the 1 from the US dialing code

    if (magicNumber.length == 10)
    {
        magicNumber = magicNumber.replace(/(\d{3})(\d{3})(\d{4})/, "($1) $2-$3");
        // Formats the 10-digit number into the form (xxx) yyy-zzzz
    } else
    {
        console.log("ERROR: Magic number could not be formatted. Check your tokens file.");
    }

    $("#phone-number-subtext").text("The magic number is " + magicNumber + ",");
}
