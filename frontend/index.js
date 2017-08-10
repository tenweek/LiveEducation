var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = 9000

io.on('connection', function(socket){
    socket.on('join', function (roomId) {
        socket.join(roomId)
    })
    socket.on('drawing', function(data, roomId){
        io.to(roomId).emit('drawing', data)
    });
});

http.listen(port, () => console.log('listening on port ' + port));
