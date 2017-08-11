<template>
    <div class="video-display">
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
        <div>
            <div class="panel-body">
                <button id="join" @click="join">Join</button>
                <button id="leave" @click="leave">Leave</button>
            </div>
        </div>
        <div id="video">
            <template v-if="this.isTeacher === true">
                <div id="agora-local" class="agora-video"></div>
            </template>
            <template v-else-if="this.isTeacher === false">
                <div id="agora-remote" class="agora-video"></div>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    name: 'video-display',
    props: ['id', 'teacherName', 'username'],
    data: function () {
        return {
            client: '',
            localStream: '',
            microphone: '',
            audioSelect: '',
            videoSelect: '',
            key: '9b343e8aaaa144928e093b29513634e9',
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
    },
    methods: {
        join: function () {
            document.getElementById('join').disabled = true
            document.getElementById('leave').disabled = false
            this.client = AgoraRTC.createClient({ mode: 'interop' })
            this.client.init(this.key, () => {
                this.client.join(null, this.id, null, (uid) => {
                    if (this.isTeacher === true) {
                        this.camera = videoSource.value
                        this.microphone = audioSource.value
                        this.localStream = AgoraRTC.createStream({
                            streamID: uid,
                            audio: true,
                            cameraId: this.camera,
                            microphoneId: this.microphone,
                            video: this.isTeacher,
                            screen: false
                        })
                        if (this.isTeacher === true) {
                            this.localStream.setVideoProfile('720p_3')
                        }
                        this.localStream.init(() => {
                            this.localStream.play('agora-local')
                            this.client.publish(this.localStream, function (err) {
                                console.log('Publish local stream error: ' + err)
                            })
                        }, function (err) {
                            console.log('getUserMedia failed', err)
                        })
                    }
                }, function (err) {
                    console.log('Join channel failed', err)
                })
            }, function (err) {
                console.log('AgoraRTC client init failed', err)
            })
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
            this.client.on('stream-added', (evt) => {
                this.client.subscribe(evt.stream, function (err) {
                    console.log('Subscribe stream failed', err)
                })
            })
            this.client.on('stream-subscribed', function (evt) {
                var stream = evt.stream
                stream.play('agora-remote')
            })
            this.client.on('stream-removed', function (evt) {
                var stream = evt.stream
                stream.stop()
                $('#agora-remote' + stream.getId()).remove()
            })
        },
        leave: function () {
            document.getElementById('leave').disabled = true
            document.getElementById('join').disabled = false
            this.client.leave(function () {
                console.log('Leavel channel successfully')
            }, function (err) {
                console.log('Leave channel failed', err)
            })
        },
        getDevices: function () {
            AgoraRTC.getDevices(function (devices) {
                for (var i = 0; i !== devices.length; ++i) {
                    var device = devices[i]
                    var option = document.createElement('option')
                    option.value = device.deviceId
                    if (device.kind === 'audioinput') {
                        option.text = device.label || 'microphone ' + (this.audioSelect.length + 1)
                        this.audioSelect.appendChild(option)
                    } else if (device.kind === 'videoinput') {
                        option.text = device.label || 'camera ' + (this.videoSelect.length + 1)
                        this.videoSelect.appendChild(option)
                    } else {
                        console.log('Some other kind of source/device: ', device)
                    }
                }
            })
        }
    }
}
</script>

<style scoped>
.agora-video {
    width: 340px;
    height: 160px;
    display: inline-block;
}

#divDevice {
    display: none;
}

#video {
    margin: 0px auto;
}
</style>
