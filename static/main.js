$(document).ready(function()
{
    var socket = io.connect("http://" + document.domain + ":" + location.port);
    socket.on("connect", function()
    {
        socket.emit("joined", {});
        console.log("A user just accessed the site.");
    });

    socket.on("addTally", function()
    {
        console.log("Tally added!");
        addUser();
    });

    socket.on("removeTally", function()
    {
        console.log("Tally removed!");
        $("i:last-child", "#tallyIcons").remove();
        // Gets the last i element of tallyIcons and removes it
    });

    socket.on("setupTallies", function(data)
    {
        console.log("Tallies set up!");
        for(i=0; i<data.numUsers; i++)
        {
            addUser();
        };
    });

    socket.on("resetTallies", function()
    {
        console.log("Tallies reset!");
        $("#tallyIcons").empty();
    });
});

function addUser()
{
    $("#tallyIcons").append('<i class="fa fa-user"></i>');
    // TODO: For flavor, make this append a random icon.
    // The icon should be synced across users, so probably do it this way:
    // Initialize array of fa-icons in run.py or separate file.
    // In the addUser emit, pass a random icon as a param
    //
}
