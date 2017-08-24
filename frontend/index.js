let app = require('express')()
let server = require('http').Server(app)
let io = require('socket.io')(server)
let fs = require('fs')
const readline = require('readline')

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
// 记录不同房间的路径
let path = {}
// 记录不同房间的开始状态
let started = {}
// 记录基础路径
const basicPath = './static/'
let messages = []
let play = false
// .0是白板 .1是聊天室 .2是课件展示 .3是代码编辑器

function readFile(rl) {
    rl.on('line', (line) => {
        let json = eval('(' + line + ')')
        messages.push(json)
    })
}

function sendNextMessage(old_msg, io) {
    let list = messages
    if (list.length <= 0) {
        console.log('record finish')
        return
    }
    if (play) {
        let msg = list.shift()
        const time_slot = msg['time'] - old_msg['time'] > 0 ? msg['time'] - old_msg['time'] : 1
        sendMessage(io, msg)
        setTimeout(() => {
            sendNextMessage(msg, io)
        }, time_slot)
    }
}

function sendMessage(io, json) {
    console.log(json)
    if (json['type'] === 'chatroom') {
        io.to('chatboard').emit('chatroom', json)
    } else if (json['type'] === 'file') {
        io.to('file').emit('filedisplay', json)
    } else if (json['type'] === 'code') {
        io.to('code').emit('code', json)
    } else if (json['type'] === 'changeComponents') {
        io.to('tools').emit('changeCurrent', json)
    } else {
        io.to('whiteboard').emit('whiteboard', json)
    }
}

io.on('connection', function (socket) {
    let id = 0
    let idForLeave = 0
    // 向录播间广播
    socket.on('joinTest', function (roomId, account) {
        socket.join(account)
        if (messages.length === 0) {
            console.log('empty')
            const rl = readline.createInterface({
                input: fs.createReadStream(String(basicPath + roomId + '/' + roomId + '.txt'))
            });
            readFile(rl)
        }
    })

    // 加入房间
    socket.on('joinRoom', function (roomId) {
        console.log('room connected')
        socket.join(roomId)
        if (started[roomId]) {
            io.to(roomId).emit('startVideo')
        }
    })
    socket.on('pause', (account) => {
        play = !play
        if (play && messages.length > 0) {
            console.log('send')
            sendNextMessage(messages.shift(), io)
        }
    })
    // 四个管道的加入
    socket.on('join', function (roomId, realRoom) {
        id = realRoom
        idForLeave = roomId
        console.log('chatroom connected')
        if (!onlineCount[id]) {
            onlineCount[id] = 0
        }
        path[id] = basicPath + id + '/' + id + '.txt'
        onlineCount[id] += 1
        socket.join(roomId)
        if (started[realRoom]) {
            io.to(roomId).emit('getStarted')
        }
        io.to(roomId).emit('changeNum', onlineCount[id])
    })
    socket.on('joinForWhiteBoard', function (roomId) {
        console.log('whiteboard connected')
        let index = parseInt(roomId.split('.')[0])
        socket.join(roomId)
        if (started[index]) {
            io.to(roomId).emit('getStarted')
        }
        io.to(roomId).emit('newJoin')
    })
    socket.on('joinForCodeEditor', function (roomId) {
        console.log('codeeditor connected')
        socket.join(roomId)
    })
    socket.on('joinForFileDisplay', function (roomId, isTeacher) {
        let index = parseInt(roomId.split('.')[0])
        console.log('filedisplay connected')
        socket.join(roomId)
        if (!isTeacher) {
            io.to(roomId).emit('firstPicture', pictureNow[index]['teacherId'], pictureNow[index]['fileNum'], pictureNow[index]['currentPage'], pictureNow[index]['maxPage'])
        }
    })
    // 开始直播信息
    socket.on('startLive', function (roomId) {
        console.log('start live')
        let date = new Date()
        const month = date.getMonth() + 1 > 10 ? String(date.getMonth() + 1) : '0' + String(date.getMonth() + 1)
        const time = String(date.getFullYear()) + month + String(date.getDate())
        const chatroom = roomId + '.1'
        const whiteboard = roomId + '.0'
        started[roomId] = true
        io.to(roomId).emit('time', time)
        io.to(roomId).emit('startVideo')
        io.to(chatroom).emit('getStarted')
        io.to(whiteboard).emit('getStarted')
    })
    // 接收消息
    socket.on('message', function (data, roomId) {
        console.log(data['type'])
        const index = parseInt(roomId.split('.')[0])
        if (data['type'] === 'file') {
            pictureNow[index] = {
                'teacherId': data['teacherId'],
                'fileNum': data['fileNum'],
                'currentPage': data['currentPage'],
                'maxPage': data['maxPage']
            }
        }
        fs.open(String(path[index]), 'a', (err, fd) => {
            if (err) {
                throw err
            }
            data['time'] = process.uptime() * 1000
            let msg = JSON.stringify(data) + '\n'
            fs.write(fd, msg, function (err) {
                if (err) {
                    throw err
                }
                fs.closeSync(fd)
            })
        })
        io.to(roomId).emit('message', data)
    })
    // 踢人事件
    socket.on('kickOut', function (userid, roomId) {
        console.log('kick ' + userid + ' out')
        io.to(roomId).emit('kickOut', userid)
    })
    // 关闭房间
    socket.on('closeLive', function (roomId) {
        console.log('close live')
        io.to(roomId).emit('closeLive')
    })
    socket.on('click', function (data, roomId) {
        io.to(roomId).emit('click', data)
    })
    socket.on('newJoinWhiteBoardMessage', function (data, roomId) {
        io.to(roomId).emit('updateWhiteBoardMessage', data)
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

