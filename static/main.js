$(document).ready(function()
{
    var socket = io.connect("http://" + document.domain + ":" + location.port);
    socket.on("connect", function()
    {
        socket.emit("joined", {});
        console.log("A user just accessed the site.");
    });

    socket.on("addUser", function()
    {
        console.log("Add user here!");
        // TODO: Call a method that displays one more user
    });

    socket.on("removeUser", function()
    {
        console.log("Remove user here!");
        // TODO: Call a method that displays one fewer user
    });

    socket.on("setupUsers", function(data)
    {
        console.log(data);
        // TODO: Call a method that displays the current number of users in the queue
    });

    socket.on("resetUsers", function()
    {
        console.log("Remove all users from display here!");
        // TODO: Call a method that removes all users from display
    });
});
