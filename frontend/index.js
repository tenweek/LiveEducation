var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);

server.listen(9000, () => {
	console.log('in 9000')
});

io.on('connection', function (mysocket) {
	console.log('connected')
	mysocket.on('join', function (roomid) {
		mysocket.join(roomid)
	})
	mysocket.on('message', function (data, roomid) {
		console.log('received')
		io.to(roomid).emit('data', data)
	});
	mysocket.on('disconnect', function () {
		console.log('disconnect')
	})
});