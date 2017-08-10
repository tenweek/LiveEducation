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
        console.log('connected')
        onlineCount++
        socket.join(roomid)
        io.to(roomid).emit('login', onlineCount)
    })
    socket.on('message', function (data, roomid) {
        console.log('received')
        io.to(roomid).emit('message', data)
    });
    socket.on('disconnect', function () {
        console.log('disconnect')
        onlineCount--
        io.to(id).emit('logout', onlineCount)
    })
});