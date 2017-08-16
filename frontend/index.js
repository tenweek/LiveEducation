let app = require('express')()
let server = require('http').Server(app)
let io = require('socket.io')(server)

app.get('/', function (req, res) {
    res.send('<h1>Hello Wellcome</h1>')
})

server.listen(9000, () => {
    console.log('in 9000')
})

let onlineCount = 0

io.on('connection', function (socket) {
    let id = 0
    socket.on('join', function (roomid) {
        id = roomid
        console.log('chatroom connected')
        onlineCount++
        socket.join(roomid)
        io.to(roomid).emit('login', onlineCount)
    })
    socket.on('joinForWhiteBoard', function (roomId) {
        console.log('whiteboard connected')
        console.log('newJoinWB')
        socket.join(roomId)
        io.to(roomId).emit('newJoin')
    })
    socket.on('joinForCodeEditor', function (roomId) {
        console.log('codeeditor connected')
        socket.join(roomId)
    })
    socket.on('joinForFileDisplay', function (roomId) {
        console.log('filedisplay connected')
        socket.join(roomId)
    })
    socket.on('message', function (data, roomid) {
        console.log('received')
        io.to(roomid).emit('message', data)
    })
    socket.on('kickOut', function (userid, roomid) {
        console.log('kick ' + userid + ' out')
        io.to(roomid).emit('kickOut', userid)
    })
    socket.on('drawing', function (data, roomId) {
        io.to(roomId).emit('drawing', data)
    })
    socket.on('click', function (data, roomId) {
        io.to(roomId).emit('click', data)
    })
    socket.on('newJoinWhiteBoardMessage', function (data, roomId) {
        io.to(roomId).emit('updateWhiteBoardMessage', data)
    })
    socket.on('disconnect', function () {
        console.log('disconnect')
        onlineCount--
        io.to(id).emit('logout', onlineCount)
    })
});
