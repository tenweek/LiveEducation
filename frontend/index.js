let app = require('express')()
let server = require('http').Server(app)
let io = require('socket.io')(server)
let fs = require('fs')

app.get('/', function (req, res) {
    res.send('<h1>Hello Wellcome</h1>')
})

server.listen(9000, () => {
    console.log('in 9000')
})

// 记录房间当前人数
let onlineCount = {}
// 记录房间当前PPT页码
let pictureNow = {}
// 记录基础路径
const basicPath = './static/'

io.on('connection', function (socket) {
    let id = 0
    let idForLeave = 0
    let nowPath = basicPath + '22/22.txt'
    // 这个起始时间应该要进行修改
    const TIME = process.uptime() * 1000
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
    socket.on('joinForFileDisplay', function (roomId) {
        console.log('filedisplay connected')
        socket.join(roomId)
        io.to(roomId).emit('firstPicture', pictureNow[id])
    })
    socket.on('fileDisplayMessage', function (data, roomId) {
        console.log('fileDisplayMessage')
        pictureNow[id] = data
        io.to(roomId).emit('fileDisplayMessage', data)
    })
    socket.on('codeMessage', function (data, roomId) {
        console.log('codeMessage')
        fs.open(nowPath, 'a', (err, fd) => {
            if (err) {
                throw err
            }
            let now = process.uptime() * 1000 - TIME
            let message = now + 'code\n' + data + '\n'
            fs.write(fd, message, function (err) {
                if (err) {
                    throw err
                }
                fs.closeSync(fd)
            })
        })
        io.to(roomId).emit('message', data)
    })
    socket.on('message', function (data, roomId) {
        console.log('chatroomMessage')
        fs.open(nowPath, 'a', (err, fd) => {
            if (err) {
                throw err
            }
            // let isTeacher = data['isTeacher'] ? 'T' : 'F'
            // let now = process.uptime() * 1000 - TIME
            // let message = now + 'chatroom\n' + isTeacher + ':' + data['message'] + '\n'
            let msg = JSON.stringify(data)
            let now = process.uptime() * 1000 - TIME
            let message = now + 'chatroom\n' + msg + '\n'
            fs.write(fd, message, function (err) {
                if (err) {
                    throw err
                }
                fs.closeSync(fd)
            })
        })
        io.to(roomId).emit('message', data)
    })
    socket.on('kickOut', function (userid, roomId) {
        console.log('kick ' + userid + ' out')
        io.to(roomId).emit('kickOut', userid)
    })
    socket.on('drawing', function (data, roomId) {
        console.log('drawboardMessage')
        fs.open(nowPath, 'a', (err, fd) => {
            if (err) {
                throw err
            }
            let msg = JSON.stringify(data)
            let now = process.uptime() * 1000 - TIME
            let message = now + 'whiteboard\n' + msg + '\n'
            fs.write(fd, message, function (err) {
                if (err) {
                    throw err
                }
                fs.closeSync(fd)
            })
        })
        io.to(roomId).emit('whiteboardMessage', data)
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
