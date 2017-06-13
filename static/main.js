/* var app = require('http').createServer(handler)
var io = require('socket.io')(app);
var fs = require('fs');

app.listen(80);

function handler (req, res) {
  fs.readFile(__dirname + '/index.html',
  function (err, data) {
    if (err) {
      res.writeHead(500);
      return res.end('Error loading index.html');
    }

    res.writeHead(200);
    res.end(data);
  });
}

io.on('connection', function (socket) {
  socket.emit('news', { hello: 'world' });
  socket.on('my other event', function (data) {
    console.log(data);
  });
}); */


$(document).ready(function(){
  console.log("JQUERY IS INSTALLED");
  // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
  // this is a callback that triggers when the "my response" event is emitted by the server.
  socket.on('my response', function(msg) {
      $('#log').append('<p>Received: ' + msg.data + '</p>');
  });
});
