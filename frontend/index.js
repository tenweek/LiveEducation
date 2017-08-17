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
// 记录基础路径
const basicPath = './static/'

// .0是白板 .1是聊天室 .2是课件展示 .3是代码编辑器

io.on('connection', function (socket) {
    let id = 0
    let idForLeave = 0
    // 这个起始时间应该要进行修改
    const TIME = process.uptime() * 1000
    socket.on('joinTest', function (roomId) {
        console.log('聊天室加入')
        socket.join(roomId)
        // 像聊天室打印信息
        const rl = readline.createInterface({
            input: fs.createReadStream(basicPath + '23/23.txt')
        });
        rl.on('line', (line) => {
            let json = eval('('+line+')')
            console.log(json)
            if (json['type'] === 'chatroom') {
                io.to(roomId).emit('chatroom', json)
            }else if (json['type']==='file'){
                console.log('file')
            }else if(json['type']==='code'){
                console.log('code')
            }else {
                console.log('whiteboard')
            }
        })
    })
    // 加入房间 用于广播是否开始直播
    socket.on('joinRoom', function (roomId) {
        console.log('room connected')
        socket.join(roomId)
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
        let index = parseInt(roomId.split('.')[0])
        console.log('filedisplay connected')
        socket.join(roomId)
        if (pictureNow[index]) {
            io.to(roomId).emit('firstPicture', pictureNow[index])
        }
    })
    // 开始直播信息
    socket.on('startLive', function (roomId) {
        console.log('start live')
        const chatroom = roomId + '.1'
        const whiteboard = roomId + '.0'
        io.to(chatroom).emit('getStarted')
        io.to(whiteboard).emit('getStarted')
    })
    // 接收消息
    socket.on('message', function (data, roomId) {
        console.log(data['type'])
        if (data['type'] === 'file') {
            let index = parseInt(roomId.split('.')[0])
            pictureNow[index] = data['page']
        }
        const index = parseInt(roomId.split('.')[0])
        fs.open(path[index], 'a', (err, fd) => {
            if (err) {
                throw err
            }
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
    // 监听退出事件
    socket.on('disconnecting', function (resaon) {
        const rooms = Object.keys(socket.rooms)
        if (rooms[1] === idForLeave) {
            console.log('disconnect')
            onlineCount[id] -= 1
            io.to(id).emit('changeNum', onlineCount[id])
        }
    })
});

