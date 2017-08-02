<template>
    <div class="get-test">
        <button class="new-button" @click="showdata"> Get Test! </button>
    </div>
</template>

<script>
export default {
  name: 'get-test',
  data () {
    return {}
  },
  methods: {
    showdata () {
      fetch('get-test', {
        method: 'get',
        mode: 'cors'
      }).then((response) => response.json()).then((obj) => {
        alert(obj.msg)
                // console.log(obj.msg)
      })
    }
  }
}
</script>