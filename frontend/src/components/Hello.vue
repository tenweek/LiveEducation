<template>
    <div>
        <router-link to="/signup">注册</router-link>
    </div>
</template>

<script>
import SignUp from './SignUp'

export default {
    name: 'Hello',
    components: {
        SignUp
    },
    data () {
        return {}
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>