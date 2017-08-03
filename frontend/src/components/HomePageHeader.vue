<template>
    <div class="title">
        <div class="logo">
            <img src="../assets/rabbit.jpg" height="60">
            <label id="mdzz">MDZZ</label>
        </div>
    </div>
</template>

<script>
    export default {
    name: 'home-page-header',
    components: {
    },
    data() {
        return {}
    },
    methods: {
    }
}
</script>

<style scoped>
    .title{
        height: 60px;
        line-height:60px;
        width: 100%;
        padding-left: 30px;
        background: white;
    }
    .logo{
        width: 180px;
        height: 100%;
    }
    #mdzz{
        color: #464c5b;
        vertical-align: top;
    }
</style>