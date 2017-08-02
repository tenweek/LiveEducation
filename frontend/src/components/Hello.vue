<template>
    <div>
        <router-link to="/signin">注册</router-link>
    </div>
</template>

<script>
import SignUp from './SignUp'

export default {
    name: 'hello',
    components: {
        SignUp,
    },
    data() {
        return {}
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>