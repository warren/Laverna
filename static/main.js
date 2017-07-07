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
        console.log("Time left is " + data.seconds);
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
    // TODO: Set up initial timer
    var x = setInterval(function()
    {
        secondsLeft = secondsLeft - 1;
        $("#timer-subtext").text("and the next round will begin in " + secondsLeft + " seconds.");
    })
}

function setupPhoneNumber(magicNumber)
{
    $("#phone-number-subtext").text("The magic number is " + magicNumber + ",");
}
