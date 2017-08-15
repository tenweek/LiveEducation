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
        <div class="control-panel">
            <Button @click="join"><Icon id="join" type="android-arrow-dropright-circle"></Icon></Button>
            <template v-if="this.username !== this.teacherName">
                <Button @click="play"><Icon id="play" type="play"></Icon></Button>
                <Button @click="pause"><Icon id="pause" type="pause"></Icon></Button>
                <Button @click="mute"><Icon id="volume" type="volume-high"></Icon></Button>
            </template>
            <template v-else-if="this.username === this.teacherName">
                <Button @click="publish"><Icon id="publish" type="play"></Icon></Button>
                <Button @click="unpublish"><Icon id="unpublish" type="stop"></Icon></Button>
            </template>
            <Button @click="showVideo"><Icon id="arrow" type="chevron-up"></Icon></Button>
        </div>
        <div id="video">
            <template v-if="this.username === this.teacherName">
                <div id="agora-local"></div>
            </template>
            <template v-else-if="this.username !== this.teacherName">
                <div id="agora-remote"></div>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    name: 'video-display',
    props: ['roomId', 'teacherName', 'username'],
    data: function () {
        return {
            client: '',
            localStream: '',
            remoteStream: '',
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
    },
    methods: {
        showVideo: function () {
            let video = document.getElementById('video')
            let arrow = document.getElementById('arrow')
            if (video.style.display === 'none') {
                video.style.display = 'inline-block'
                arrow.type = 'chevron-up'
            } else {
                video.style.display = 'none'
                arrow.type = 'chevron-down'
            }
        },
        play: function () {
            document.getElementById('play').disable = true
            document.getElementById('pause').disable = false
            this.remoteStream.enableVideo()
        },
        pause: function () {
            document.getElementById('play').disable = false
            document.getElementById('pause').disable = true
            this.remoteStream.disableVideo()
        },
        mute: function () {
            let volume = document.getElementById('volume')
            if (volume.type === 'volume-high') {
                this.remoteStream.disableAudio()
                volume.type = 'android-volume-mute'
            } else {
                this.remoteStream.enableAudio()
                volume.type = 'volume-high'
            }
        },
        publish: function () {
            document.getElementById('unpublish').disable = false
            document.getElementById('publish').disable = true
            this.client.publish(this.localStream, function (err) {
                console.log('Publish local stream error: ' + err)
            })
        },
        unpublish: function () {
            document.getElementById('publish').disable = false
            document.getElementById('unpublish').disable = true
            this.client.unpublish(this.localStream, function (err) {
                console.log('Unpublish local stream failed' + err)
            })
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
            console.log('Init AgoraRTC client with vendor key:')
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
        },
        monitorStream: function () {
            this.client.on('stream-added', (evt) => {
                this.client.subscribe(evt.stream, function (err) {
                    console.log('Subscribe stream failed', err)
                })
            })
            this.client.on('stream-subscribed', function (evt) {
                this.remoteStream = evt.stream
                this.remoteStream.play('agora-remote')
            })
            this.client.on('stream-removed', function (evt) {
                var stream = evt.stream
                stream.stop()
            })
            this.client.on('peer-leave', function (evt) {
                var stream = evt.stream
                if (stream) {
                    stream.stop()
                    console.log(evt.uid + ' leaved from this channel')
                }
            })
        },
        leave: function () {
            this.client.leave(function () {
                console.log('Leavel channel successfully')
            }, function (err) {
                console.log('Leave channel failed', err)
            })
        },
        getDevices: function () {
            AgoraRTC.getDevices(function (devices) {
                for (var i = 0; i !== devices.length; ++i) {
                    let device = devices[i]
                    let option = document.createElement('option')
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
#agora-local, #agora-remote {
    width: 100%;
    height: 100%;
    display: inline-block;
}

#video {
    width: 100%;
    height: 23vmin;
}

#divDevice {
    display: none;
}
</style>
