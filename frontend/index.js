var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);

//服务器在9000监听
server.listen(9000,() => {
	console.log('in 9000')
});

//io监听连接事件
io.on('connection', function (mysocket) {
	console.log('connected')
  //监听加入房间事件
	mysocket.on('join',function(roomid){
		mysocket.join(roomid)
	})
  //监听message事件
  mysocket.on('message',function(msg,roomid){
  	console.log('received')
    console.log(roomid)
  	io.to(roomid).emit('message',msg)  //向roomid号房间发送消息
  });
  //监听断开连接时件
  mysocket.on('disconnect', function(){
  	console.log('disconnect')
  })
});