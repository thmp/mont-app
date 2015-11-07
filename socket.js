var io = require('socket.io'),
    ioServer = io.listen(8000);


console.log('Socket.io listening at port %d', 8000);


// Chatroom
ioServer.on('connection', function (socket) {
  
  console.info('New client connected (id=' + socket.id + ').');

  // when the client emits 'new message', this listens and executes
  socket.on('sendMsg', function (data) {
    console.log('New message: ' + data + ', socket.id: ' + socket.id)
    // we tell the client to execute 'new message'
    socket.broadcast.emit('recMsg', {
      message: data
    });
  });
  
});
