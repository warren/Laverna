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
        addUser(data.iconName);
        // data.iconName is a string containing the name of the chosen fa-icon
        console.log("Tally added!");
    });

    socket.on("removeTally", function(data)
    {
        $("i:." + data.iconName, "#tallyIcons").remove();
        // Removes all i elements of tallyIcons that have the class name iconName
        console.log("Tally with id " + data.iconName + "removed!");
    });

    socket.on("setup", function(data)
    {
        setupTallies(data.iconList);
        console.log("Time left is " + data.seconds);
        console.log("Magic number is " + data.magicNumber);

    });

    socket.on("resetTallies", function()
    {
        $("#tallyIcons").empty();
        console.log("Tallies reset!");
    });

    // TODO: Make a setup socket that gets timer details and phone number
});

function setupTallies(iconList)
{
    for(i=0; i<iconList.length; i++)
    {
        $("#tallyIcons").append('<i class="fa ' + iconList[i] + '"></i>');
    };
    console.log("Tallies set up!");
}
