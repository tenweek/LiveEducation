var app = require('express')()
var server = require('http').Server(app)
var io = require('socket.io')(server)

app.get('/', function (req, res) {
    res.send('<h1>Hello Wellcome</h1>')
})

server.listen(9000, () => {
    console.log('in 9000')
})

var onlineCount = {}
var pictureNow = {}

io.on('connection', function (socket) {
    var id = 0
    var idForLeave = 0
    socket.on('join', function (roomId, realRoom) {
        id = realRoom
        idForLeave = roomId
        console.log('chatroom connected')
        if (!onlineCount[id]) {
            onlineCount[id] = 0
        }
        onlineCount[id] += 1
        socket.join(roomId)
        io.to(roomId).emit('changeNum', onlineCount[id])
    })
    socket.on('joinForWhiteBoard', function (roomId) {
        console.log('whiteboard connected')
        socket.join(roomId)
    })
    socket.on('joinForCodeEditor', function (roomId) {
        console.log('codeeditor connected')
        socket.join(roomId)
    })
    socket.on('joinForFileDisplay', function (roomId, id, isTeacher) {
        console.log('filedisplay connected')
        socket.join(roomId)
        if (!isTeacher) {
            io.to(roomId).emit('firstPicture', pictureNow[id]['teacherId'], pictureNow[id]['fileNum'], pictureNow[id]['currentPage'], pictureNow[id]['maxPage'])
        }
    })
    socket.on('fileDisplayMessage', function (teacherId, fileNum, currentPage, maxPage, roomId, id) {
        console.log('received')
        pictureNow[id] = {'teacherId': teacherId, 'fileNum': fileNum, 'currentPage': currentPage, 'maxPage': maxPage}
        io.to(roomId).emit('fileDisplayMessage', teacherId, fileNum, currentPage, maxPage)
    })
    socket.on('message', function (data, roomId) {
        console.log('received')
        io.to(roomId).emit('message', data)
    })
    socket.on('kickOut', function (userid, roomId) {
        console.log('kick ' + userid + ' out')
        io.to(roomId).emit('kickOut', userid)
    })
    socket.on('drawing', function (data, roomId) {
        io.to(roomId).emit('drawing', data)
    })
    socket.on('disconnecting', function (resaon) {
        const rooms = Object.keys(socket.rooms)
        if (rooms[1] === idForLeave) {
            console.log('disconnect')
            onlineCount[id] -= 1
            io.to(id).emit('changeNum', onlineCount[id])
        }
    })
});
