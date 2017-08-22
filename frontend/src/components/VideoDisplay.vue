<template>
    <Card id="video-display">
        <div id="divDevice">
            <div class="select">
                <label for="audioSource">Audio source: </label>
                <select id="audioSource"></select>
            </div>
            <div class="select">
                <label for="videoSource">Video source: </label>
                <select id="videoSource"></select>
            </div>
        </div>
        <div id="video">
            <template v-if="this.username === this.teacherName">
                <div id="agora-local">
                    <div class="control-panel">
                        <Button @click="play" id="play" type="ghost" shape="circle" icon="play"></Button>
                        <Button @click="stop" id="stop" type="ghost" shape="circle" icon="stop"></Button>
                    </div>
                </div>
            </template>
            <template v-else>
                <div id="agora-remote"></div>
            </template>
        </div>
    </Card>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'

/**
 * 视频直播区域
 *
 * @module VideoDisplay
 * @class VideoDisplay
 */
export default {
    name: 'video-display',
    /**
     * 表示房间ID号
     *
     * @property roomId
     * @type String
     */

    /**
     * 表示创建该房间的老师名字
     *
     * @property teacherName
     * @type String
     */

    /**
     * 表示进入该房间的用户名字
     *
     * @property username
     * @type String
     */
    props: ['roomId', 'teacherName', 'username', 'containerHeight'],
    data: function () {
        return {
            /**
             * client对象
             *
             * @attribute client
             * @type String
             * @default ''
             */
            client: '',
            /**
             * 表示本地音视频流
             *
             * @attribute localStream
             * @type String
             * @default ''
             */
            localStream: '',
            /**
             * 表示用户的麦克风
             *
             * @attribute microphone
             * @type String
             * @default ''
             */
            microphone: '',
            /**
             * 表示用户麦克风的权限
             *
             * @attribute audioSelect
             * @type String
             * @default ''
             */
            audioSelect: '',
            /**
             * 表示用户摄像头的权限
             *
             * @attribute videoSelect
             * @type String
             * @default ''
             */
            videoSelect: '',
            /**
             * 声网提供的项目的aapID
             *
             * @attribute appKey
             * @readOnly
             * @type String
             * @default '9b343e8aaaa144928e093b29513634e9'
             */
            appKey: '9b343e8aaaa144928e093b29513634e9',
            /**
             * 表示用户的摄像头
             *
             * @attribute camera
             * @type String
             * @default ''
             */
            camera: '',
            socket: ''
        }
    },
    /**
     * created函数
     *
     * @method created
     */
    created: function () {
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('joinRoom', this.roomId)
    },
    /**
     * mounted函数，初始化相关数据
     *
     * @method mounted
     */
    mounted: function () {
        this.audioSelect = document.querySelector('select#audioSource')
        this.videoSelect = document.querySelector('select#videoSource')
        document.getElementById('video').style.height = (this.containerHeight - 32) + 'px'
        let self = this
        self.socket.on('startVideo', function () {
            self.join()
        })
    },
    methods: {
        /**
         * 播放视频
         *
         * @method play
         */
        play: function () {
            document.getElementById('stop').style.display = 'inline-block'
            document.getElementById('play').style.display = 'none'
            this.localStream.enableVideo()
        },
        /**
         * 停止播放视频
         *
         * @method
         */
        stop: function () {
            document.getElementById('play').style.display = 'inline-block'
            document.getElementById('stop').style.display = 'none'
            this.localStream.disableVideo()
        },
        /**
         * 老师开始直播
         *
         * @method join
         */
        join: function () {
            this.clientInit()
            this.client.on('error', function (err) {
                console.log('Got error msg:', err.reason)
                if (err.reason === 'DYNAMIC_KEY_TIMEOUT') {
                    this.client.renewChannelKey('', function () {
                        console.log('Renew channel key successfully')
                    }, function (err) {
                        console.log('Renew channel key failed: ', err)
                    })
                }
            })
            this.monitorStream()
        },
        /**
         * 初始化client对象
         *
         * @method clientInit
         */
        clientInit: function () {
            this.client = AgoraRTC.createClient({ mode: 'interop' })
            this.client.init(this.appKey, () => {
                this.client.join(null, this.roomId, null, (uid) => {
                    if (this.username === this.teacherName) {
                        this.camera = videoSource.value
                        this.microphone = audioSource.value
                        this.localStream = AgoraRTC.createStream({
                            streamID: uid,
                            audio: true,
                            cameraId: this.camera,
                            microphoneId: this.microphone,
                            video: true,
                            screen: false
                        })
                        this.localStream.setVideoProfile('720p_3')
                        this.localStream.init(() => {
                            this.localStream.play('agora-local')
                            this.client.publish(this.localStream)
                        })
                    }
                })
            })
        },
        /**
         * 监测音视频流的状态并根据事件执行回调函数
         *
         * @method monitorStream
         */
        monitorStream: function () {
            this.client.on('stream-added', (evt) => {
                this.client.subscribe(evt.stream)
            })
            this.client.on('stream-subscribed', function (evt) {
                let stream = evt.stream
                stream.play('agora-remote')
            })
            this.client.on('stream-removed', function (evt) {
                let stream = evt.stream
                stream.stop()
            })
            this.client.on('peer-leave', function (evt) {
                let stream = evt.stream
                if (stream) {
                    stream.stop()
                }
            })
        },
        /**
         * 关闭直播视频
         *
         * @method leave
         */
        leave: function () {
            this.client.leave()
        },
        /**
         * 获取用户设备（用户的麦克风和摄像头的使用权限）
         *
         * @method getDevices
         */
        getDevices: function () {
            AgoraRTC.getDevices(function (devices) {
                for (let i = 0; i !== devices.length; ++i) {
                    let device = devices[i]
                    let option = document.createElement('option')
                    option.value = device.deviceId
                    if (device.kind === 'audioinput') {
                        option.text = device.label || 'microphone ' + (this.audioSelect.length + 1)
                        this.audioSelect.appendChild(option)
                    } else if (device.kind === 'videoinput') {
                        option.text = device.label || 'camera ' + (this.videoSelect.length + 1)
                        this.videoSelect.appendChild(option)
                    }
                }
            })
        }
    },
    watch: {
        containerHeight: function (newVal, oldVal) {
            document.getElementById('video').style.height = (newVal - 32) + 'px'
        }
    }
}
</script>

<style scoped>
#agora-local,
#agora-remote {
    width: 100%;
    height: 100%;
    display: inline-block;
}

#video-display,
#video {
    width: 100%;
    height: 100%;
}

#video {
    position: relative;
}

#divDevice {
    display: none;
}

#play {
    display: none;
}

.control-panel {
    text-align: right;
    position: absolute;
    z-index: 50;
    right: 0;
}
</style>
