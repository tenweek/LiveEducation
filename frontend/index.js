var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var nsp = io.of('/mynsp');
var nsp1 = io.of('/mynsp1');

app.get('/', function(req, res){
  res.sendFile(__dirname+'/index.html');
});



nsp.on('connection', function(socket){
	console.log('user in nsp connected');
	socket.on('chat message', function(msg){
    nsp.emit('chat message',msg);
  });
	socket.on('disconnect',function(){
		console.log('user in nsp disconnected')
	})
})

nsp1.on('connection', function(socket){
	console.log('user in nsp1 connected');
	socket.on('chat message', function(msg){
    nsp1.to(1).emit('chat message',msg);
  });
	socket.on('join',function() {
		socket.join(1);
		console.log('in room 1 succefully')
	})
	socket.on('disconnect',function(){
		console.log('user in nsp1 disconnected')
	})
})

http.listen(8000, function(){
  console.log('listening on *:8000');
});