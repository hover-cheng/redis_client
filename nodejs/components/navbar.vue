<template lang="html">
  <div class="ui basic segment">
    <div class="ui visible vertical left sidebar menu">
      <a class="item">
        <h2 class="ui center aligned icon header">
          <img src="~/static/img/patrick.png" class="ui circular image"> <p>{{ username}}</p>
        </h2>
      </a>
      <div v-for="(item,i) in result">
        <a class="item" @click="getRedisId(i)">
          <h4 class="ui center aligned header">{{item.projectname}}-{{item.redisname}}</h4>
        </a>
      </div>
      <a class="item">
        <h4 class="ui center aligned header" @click="addredis()"><i class="plus icon"></i></h4>
      </a>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  props: ["redisId", "isActive", "op", "url", "usertoken", "isshow", "wssock"],
  data() {
    return {
      username: '',
      result: [],
      token: '',

    }
  },
  methods: {
    getRedisList: function () {
      axios.get('http://127.0.0.1:8000/api/redislist', {headers: {'Authorization':"Bearer "+ this.token}})
      .then(res=>{
        this.result =res.data
      })
      .catch((err) => {
        alert("Token is invalid or expired");
        window.location.href= "/login";
      })
    },
    getRedisId: function (id) {
      let rinfo = this.result[id]
      if (this.wssock) {
        this.wssock.send(JSON.stringify({"cmd0": "close"}))
      }
      this.$emit("update:redisId", rinfo)
      this.$emit("update:isshow", false)
    },
    addredis: function () {
      if (this.wssock) {
        this.wssock.send('close')
      }
      this.redisId = ''
      this.$emit("update:op", "POST")
      this.$emit("update:url", "http://127.0.0.1:8000/api/redislist")
      this.$emit("update:isActive", "active")
      this.$emit("update:isshow", false)
    },
    getUsername: function () {
      axios.get('http://127.0.0.1:8000/api/redislist/username', {headers: {'Authorization':"Bearer "+ this.token}})
      .then(res=>{
        this.username = res.data.username
      })
      .catch((err) => {console.log("Token is invalid or expired");})
    }
  },
  watch: {
    token: function (val) {
      this.$emit("update:usertoken", val)
    }
  },
  mounted: function () {
    this.token = window.localStorage.getItem("usertoken")?window.localStorage.getItem("usertoken"): ''
    this.getRedisList()
    this.getUsername()
    // this.username =window.localStorage['username']
  },
}
</script>

<style lang="css" scoped>
.ui.visible.vertical.left.sidebar.menu {
  background-color: rgb(8, 69, 99);
  width:220px;
}
.ui.center.aligned.header {
  color:white;
}

</style>
