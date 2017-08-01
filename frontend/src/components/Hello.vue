<template>
    <div>
        <test-get></test-get>
        <sign-up></sign-up>
    </div>
</template>

<script>
import TestGet from './test_get'
import SignUp from './signUp'

export default {
    name: 'hello',
    components: {
        TestGet,
        SignUp,
    },
    data() {
        return {}
    },
    methods: {}
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>