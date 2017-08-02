<template>
    <div class="make-room">
        <form>
            Room Name:
            <input type="text" id="roomname" v-model="roomname" />
            <input type="submit" value="Submit" @click="showdata" />
            <input type="submit" value="Room" @click="showroom" />
        </form>
        <ul class="room" id="room">
          <li v-for="room in rooms">
            <p readonly="true">{{room.Room}}</p>
          </li>
        </ul>
    </div>
</template>

<script>
export default {
  name: 'make-room',
  data () {
    return {
      roomname: '',
      rooms: []
    }
  },
  methods: {
    showdata () {
      fetch('make-room', {
        method: 'post',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json, text/plain, */*',
          'Accept': 'application/json'
        },
        body: JSON.stringify({'roomname': this.roomname, 'authId': 'wenbin'})
      }).then((response) => response.json()).then((obj) => {
        alert(obj.msg)
               // console.log(obj.msg)
      })
    },
    showroom () {
      fetch('list-room', {
        method: 'get',
        mode: 'cors'
      }).then((response) => response.json()).then((obj) => {
        this.rooms = obj.rooms
        // console.log(obj.rooms[1])
      })
    }
  }
}
</script>