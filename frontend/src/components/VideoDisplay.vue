<template>
    <div class="video-display">
        <div id="div_device" class="panel panel-default" style="display:none">
            <div class="select">
                <label for="audioSource">Audio source: </label>
                <select id="audioSource"></select>
            </div>
            <div class="select">
                <label for="videoSource">Video source: </label>
                <select id="videoSource"></select>
            </div>
        </div>
        <div id="div_join" class="panel panel-default">
            <div class="panel-body">
                <button id="is-teacher" @click="teacher">not teacher</button>
                <button id="join" class="btn btn-primary" @click="join">Join</button>
                <button id="leave" class="btn btn-primary" @click="leave">Leave</button>
                <!--button id="publish" class="btn btn-primary" @click="publish">Publish</button>
                <button id="unpublish" class="btn btn-primary" @click="unpublish">Unpublish</button-->
            </div>
        </div>
        <div id="video" style="margin:0 auto;">
            <template v-if="this.isTeacher === true">
                <div id="agora_local" style="width:210px;height:147px;display:inline-block;"></div>
            </template>
            <template v-else-if="this.isTeacher === false">
                <div id="agora_remote" style="width:210px;height:147px;display:inline-block;"></div>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    name: 'video-display',
    data: function () {
        return {
            client: '',
            localStream: '',
            microphone: '',
            audioSelect: '',
            videoSelect: '',
            key: '9b343e8aaaa144928e093b29513634e9',
            channel: '1000',
            camera: '',
            isTeacher: true
        }
    },
    mounted: function () {
        this.audioSelect = document.querySelector('select#audioSource')
        this.videoSelect = document.querySelector('select#videoSource')
    },
    methods: {
        teacher: function () {
            this.isTeacher = false
            document.getElementById('is-teacher').disabled = true
        },
        join: function () {
            document.getElementById('join').disabled = true

            console.log('Init AgoraRTC client with vendor key: ' + this.key)
            this.client = AgoraRTC.createClient({mode: 'interop'})
            this.client.init(this.key, () => {
                console.log('AgoraRTC client initialized')
                this.client.join(null, this.channel, null, (uid) => {
                    console.log('User ' + uid + ' join channel successfully')

                    if (this.isTeacher === true) {
                        this.camera = videoSource.value
                        this.microphone = audioSource.value
                        this.localStream = AgoraRTC.createStream({streamID: uid, audio: true, cameraId: this.camera, microphoneId: this.microphone, video: this.isTeacher, screen: false})
                        if (this.isTeacher === true) {
                            this.localStream.setVideoProfile('720p_3')
                        }
                        this.localStream.init(() => {
                            console.log('getUserMedia successfully')
                            this.localStream.play('agora_local')
                            this.client.publish(this.localStream, function (err) {
                                console.log('Publish local stream error: ' + err)
                            })
                            this.client.on('stream-published', function (evt) {
                                console.log('Publish local stream successfully')
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
                var stream = evt.stream
                console.log('New stream added: ' + stream.getId())
                console.log('Subscribe ', stream)
                this.client.subscribe(stream, function (err) {
                    console.log('Subscribe stream failed', err)
                })
            })
            this.client.on('stream-subscribed', function (evt) {
                var stream = evt.stream
                console.log('Subscribe remote stream successfully: ' + stream.getId())
                stream.play('agora_remote')
            })
            this.client.on('stream-removed', function (evt) {
                var stream = evt.stream
                stream.stop()
                $('#agora_remote' + stream.getId()).remove()
                console.log('Remote stream is removed ' + stream.getId())
            })
        },
        leave: function () {
            document.getElementById('leave').disabled = true
            this.client.leave(function () {
                console.log('Leavel channel successfully')
            }, function (err) {
                console.log('Leave channel failed')
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