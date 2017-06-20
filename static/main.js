$(document).ready(function()
{
    console.log("jQuery is installed");
    // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/test");
});
