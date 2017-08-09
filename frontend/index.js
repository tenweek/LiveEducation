var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = process.env.PORT || 9000

io.on('connection', function(socket){
    console.log("connected123")
    socket.on('drawing', function(data){
        io.emit('drawing', data)
    });
});

http.listen(port, () => console.log('listening on port ' + port));
