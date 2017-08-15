let app = require('express')()
let server = require('http').Server(app)
let io = require('socket.io')(server)

app.get('/', function (req, res) {
    res.send('<h1>Hello Wellcome</h1>')
})

server.listen(9000, () => {
    console.log('in 9000')
})

let onlineCount = {}
let pictureNum = []

io.on('connection', function (socket) {
    let id = 0
    socket.on('join', function (roomid) {
        id = roomid
        console.log('chatroom connected')
        if (!onlineCount[id]) {
            onlineCount[id] = 0
        }
        onlineCount[id] += 1
        socket.join(roomid)
        io.to(roomid).emit('changeNum', onlineCount[id])
    })
    socket.on('joinForWhiteBoard', function (roomId) {
        console.log('whiteboard connected')
        socket.join(roomId)
    })
    socket.on('joinForCodeEditor', function (roomId) {
        console.log('codeeditor connected')
        socket.join(roomId)
    })
    socket.on('joinForFileDisplay', function (roomId, roomNum) {
        console.log('filedisplay connected')
        socket.join(roomId)
        io.to(roomId).emit('firstPicture', pictureNum[roomNum])
    })
    socket.on('fileDisplayMessage', function (data, roomId, roomNum) {
        console.log('received')
        pictureNum[roomNum] = data
        io.to(roomId).emit('fileDisplayMessage', data)
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
    socket.on('disconnecting', function (resaon) {
        const rooms = Object.keys(socket.rooms)
        if (rooms[1] === id) {
            onlineCount[id] -= 1
            io.to(id).emit('changeNum', onlineCount[id])
        }
    })
});
