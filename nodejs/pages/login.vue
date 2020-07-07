<template lang="html">
  <div class="loginContent">
    <div class="ui form">
      <h2 class="ui center aligned inverted header">Redis管理平台</h2>
      <div class="inline fields">
        <div class="ui left icon input">
          <input type="text" v-model="username" name="username" value="" placeholder="username">
          <i class="user icon"></i>
        </div>
      </div>
      <div class="inline fields">
        <div class="ui left icon input">
          <input type="password" v-model="password" name="password"  value="" placeholder="password" @keyup.enter="login">
          <i class="lock icon"></i>
        </div>
      </div>
    </div>
    <div class="field">
        <button class="fluid ui blue button" type="submit" name="button" @click="login">确认</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  head: {
      title: "登陆",
    // 定义body的样式
    bodyAttrs: {
      style: 'background-color: rgb(8, 69, 99)',
    }
  },
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods:{
    login: function() {
      let _this = this;
      axios.post('http://127.0.0.1:8000/api/jwt-token-auth', {"username": this.username, "password": this.password})
      .then((res) => {
        // 本地浏览器保存token和username
        window.localStorage.setItem('usertoken', res.data.access)
        window.location.href="./redis";})
      .catch((res)=>{alert("登陆失败")})
      // console.log(this.username + ':' + this.password)
    },
  },
}
</script>

<style lang="css" scoped>

.ui.left.icon.input {
  width: 100%;
}
.loginContent {
  width:400px;
  position: absolute;
  left: 50%;
  top: 40%;
  transform: translate(-50%,-50%);
}

</style>
