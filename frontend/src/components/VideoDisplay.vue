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
        <div class="control-panel">
            <button @click="join">
                <Icon id="join" type="android-arrow-dropright-circle"></Icon>
            </button>
            <template v-if="this.username === this.teacherName">
                <button @click="play" id="play">
                    <Icon type="play"></Icon>
                </button>
                <button @click="stop" id="stop">
                    <Icon type="stop"></Icon>
                </button>
            </template>
            <button @click="showVideo" id="arrow">
                <Icon type="chevron-up"></Icon>
            </button>
        </div>
        <div id="video">
            <template v-if="this.username === this.teacherName">
                <div id="agora-local"></div>
            </template>
            <template v-else>
                <div id="agora-remote"></div>
            </template>
        </div>
    </Card>
</template>

<script>
export default {
    name: 'video-display',
    props: ['roomId', 'teacherName', 'username', 'containerHeight'],
    data: function () {
        return {
            client: '',
            localStream: '',
            microphone: '',
            audioSelect: '',
            videoSelect: '',
            appKey: '9b343e8aaaa144928e093b29513634e9',
            camera: '',
            isTeacher: false
        }
    },
    created: function () {
        this.isTeacher = this.username === this.teacherName
    },
    mounted: function () {
        this.audioSelect = document.querySelector('select#audioSource')
        this.videoSelect = document.querySelector('select#videoSource')
        document.getElementById('video').style.height = (this.containerHeight - 62) + 'px'
    },
    methods: {
        showVideo: function () {
            let arrow = document.getElementById('arrow')
            let video = document.getElementById('video')
            if (video.style.display === 'none') {
                video.style.display = 'inline-block'
                arrow.innerHTML = '<i class="ivu-icon ivu-icon-chevron-up"></i>'
            } else {
                video.style.display = 'none'
                arrow.innerHTML = '<i class="ivu-icon ivu-icon-chevron-down"></i>'
            }
        },
        play: function () {
            document.getElementById('stop').disable = false
            document.getElementById('play').disable = true
            this.localStream.enableVideo()
        },
        stop: function () {
            document.getElementById('play').disable = false
            document.getElementById('stop').disable = true
            this.localStream.disableVideo()
        },
        join: function () {
            document.getElementById('join').disable = true
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
        leave: function () {
            this.client.leave()
        },
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
            document.getElementById('video').style.height = (newVal - 62) + 'px'
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

#video {
    width: 100%;
}

#divDevice {
    display: none;
}

button {
    background-color: rgba(0, 0, 0, 0);
    color: rgb(92, 107, 119);
    border: none;
    font-size: 20px;
    margin-right: 12px;
    outline: none;
}

.control-panel {
    text-align: right;
}
</style>
