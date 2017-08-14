var app = require('express')()
var server = require('http').Server(app)
var io = require('socket.io')(server)

app.get('/', function (req, res) {
    res.send('<h1>Hello Wellcome</h1>')
})

server.listen(9000, () => {
    console.log('in 9000')
})

let onlineCount = {}
let whiteboardChosen = {}
let fileChosen = {}
let codeChosen = {}
var pictureNum = []

io.on('connection', function (socket) {
    var id = 0
    socket.on('join', function (roomid) {
        id = roomid
        console.log('chatroom connected')
        if (!onlineCount[id]) {
            onlineCount[id] = 0
            whiteboardChosen[id] = 0
            fileChosen[id] = 0
            codeChosen[id] = 0
        }
        onlineCount[id] += 1
        socket.join(roomid)
        let k = whiteboardChosen[id] + fileChosen[id] + codeChosen[id] + 1
        let num = onlineCount[id] / k
        io.to(roomid).emit('login', num)
    })
    socket.on('joinForWhiteBoard', function (roomId) {
        if (!onlineCount[id]) {
            onlineCount[id] = 0
            whiteboardChosen[id] = 0
            fileChosen[id] = 0
            codeChosen[id] = 0
        }
        onlineCount[id] += 1
        whiteboardChosen[id] = 1
        console.log('whiteboard connected')
        socket.join(roomId)
    })
    socket.on('joinForCodeEditor', function (roomId) {
        onlineCount[id] += 1
        codeChosen[id] = 1
        console.log('codeeditor connected')
        socket.join(roomId)
    })
    socket.on('joinForFileDisplay', function (roomId, roomNum) {
        onlineCount[id] += 1
        fileChosen[id] = 1
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
    });
    socket.on('disconnect', function () {
        console.log('disconnect')
        onlineCount[id] -= 1
        let k = whiteboardChosen[id] + fileChosen[id] + codeChosen[id] + 1
        let num = onlineCount[id] / k
        io.to(id).emit('logout', num)
    })
});
