<template>
    <div>
        <router-link to="/signin">go signin</router-link>
    </div>
</template>

<script>
import SignIn from './SignIn'

export default {
    name: 'hello',
    components: {
        SignIn,
    },
    data() {
        return {}
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>