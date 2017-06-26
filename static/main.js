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
        // data.icon is a string containing the name of the chosen fa-icon
        console.log("Tally added!");
    });

    socket.on("removeTally", function(data)
    {
        $("i:." + data.iconName, "#tallyIcons").remove();
        // Removes all i elements of tallyIcons that have the class name iconName
        console.log("Tally with id " + data.iconName + "removed!");
    });

    socket.on("setupTallies", function(data)
    {
        iconList = data.iconList;
        for(i=0; i<iconList.length; i++)
        {
            addUser(iconList[i]);
        };
        console.log("Tallies set up!");
    });

    socket.on("resetTallies", function()
    {
        $("#tallyIcons").empty();
        console.log("Tallies reset!");
    });
});

function addUser(iconName)
{
    $("#tallyIcons").append('<i class="fa ' + iconName + '"></i>');
    // TODO: Make sure there are no duplicate user icons bc it could
    // cause removeTally to remove 2 icons instead of 1
}
