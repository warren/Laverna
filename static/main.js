$(document).ready(function(){
  console.log("JQUERY IS INSTALLED");
  // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
  var socket = io.connect("http://" + document.domain + ":" + location.port + "/test");
  // this is a callback that triggers when the "myevent" event is emitted by the server.
  //socket.on("myevent", function(data) {
    //console.log("received myevent emission with msg:", data.msg);
  //});
});
