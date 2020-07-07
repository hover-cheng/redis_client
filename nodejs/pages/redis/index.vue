<template lang="html">
  <div class="ui basic segment">
    <div  class="ui borderless fixed menu">
      <div class="right menu">
        <a class="item" @click="descshow=!descshow">指令说明</a>
        <a class="item" @click="logout()">
          logout
        </a>
      </div>
    </div>
    <redisid ref="redisid"
    :redisId.sync="redisId"
    :isActive.sync="isActive"
    :op.sync="op"
    :url.sync="url"
    :usertoken.sync="usertoken"
    :isshow.sync="isshow"
    :wssock="wssock"
    v-on:disconnect="closeconnect">
    </redisid>
    <div class="ui isActive inverted page dimmer" :class="isActive">
      <form class="ui form">
        <div class="field">
          <div class="inline fields">
            <div class="field">
              <h4  class="ui left floated header">redis name</h4>
            </div>
            <div class="field">
              <input type="text" v-model.trim="rdsname">
            </div>
          </div>
        </div>
        <div class="field">
          <div class="inline fields">
            <div class="field">
              <h4  class="ui left floated header">redis type</h4>
            </div>
            <div class="field">
              <select class="ui dropdown" v-model.trim="rdstype">
                <option value="">选择redis模式</option>
                <option value="Sentinel">哨兵模式</option>
                <option value="Cluster">集群模式</option>
                <option value="Single">单点模式</option>
              </select>
            </div>
          </div>
        </div>
        <div class="field">
          <div class="inline fields">
            <div class="field">
              <h4  class="ui left floated header">node list</h4>
            </div>
            <div class="field">
              <textarea rows="8" cols="500" v-model.trim="rdslist" :placeholder="placeholder"></textarea>
            </div>
          </div>
        </div>
        <div class="field" v-if="rdstype == 'Sentinel'">
          <div class="inline fields">
            <div class="field">
              <h4  class="ui left floated header">master name</h4>
            </div>
            <div class="field">
                <input type="text" v-model.trim="rdsmastername">
            </div>
          </div>
        </div>
        <div class="field">
          <div class="inline fields">
            <div class="field">
              <h4  class="ui left floated header">redis password</h4>
            </div>
            <div class="field">
              <input type="text" v-model.trim="rdspwd">
            </div>
          </div>
        </div>
        <div class="field">
          <div class="inline fields">
            <div class="field">
              <h4  class="ui left floated header">project name</h4>
            </div>
            <div class="field">
              <input type="text" v-model.trim="rdsprdname">
            </div>
          </div>
        </div>
        <div class="button field">
          <button type="button" class="ui left floated primary basic button" @click="submitredis()">提交</button>
          <button type="button" class="ui right floated negative basic button" @click="isActive=''">取消</button>
        </div>
      </form>
    </div>
    <div class="ui basic segment">
      <table class="ui celled padded table" v-if="descshow">
        <thead>
          <tr>
            <th>指令</th>
            <th>说明</th>
            <th>实例</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>info</td>
            <td>打印出redis的信息</td>
            <td>info</td>
          </tr>
          <tr>
            <td>get key</td>
            <td>打印string类型的key的value值</td>
            <td>get test</td>
          </tr>
          <tr>
            <td>hget name key</td>
            <td>打印hash类型的key的value值</td>
            <td>hget domaintoip op.hz.netease.com</td>
          </tr>
          <tr>
            <td>hgetall name</td>
            <td>打印出所有的hash类型数据的name的key和value值</td>
            <td>hgetall domaintoip</td>
          </tr>
          <tr>
            <td>slowloglen</td>
            <td>打印出redis的slow log数量</td>
            <td>slowloglen</td>
          </tr>
          <tr>
            <td>slowlog num</td>
            <td>打印出redis的slow log信息,num为可选项,如果不输入则打印出所有的slow log</td>
            <td>slowlog 或者 slowlog 1</td>
          </tr>
          <tr>
            <td>slowlogrest</td>
            <td>清除redis的slow log信息</td>
            <td>slowlogrest</td>
          </tr>
          <tr>
            <td>scan key*</td>
            <td>打印出匹配key*的string类型key值</td>
            <td>scan te*</td>
          </tr>
          <tr>
            <td>hscan name key*</td>
            <td>打印出name中配置key*的hash类型key和value数据</td>
            <td>hgetall domaintoip www*</td>
          </tr>
        </tbody>
      </table>
      <table class="ui celled padded table" v-if="Object.keys(redisId).length > 0" >
        <thead>
          <tr>
            <th class="single line">redis name</th>
            <th class="single line">redis type </th>
            <th class="center aligned">nodes list</th>
            <th class="center aligned" v-if="redisId.mastername">master name</th>
            <th class="center aligned"  v-if="redisId.password">password</th>
            <th class="center aligned">create time</th>
            <th class="center aligned">连接</th>
            <th class="center aligned">编辑</th>
            <th class="center aligned">删除</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{redisId.redisname}}</td>
            <td>{{redisId.redistype}}</td>
            <td>{{redisId.nodelist.replace(/,/g,'\n')}}</td>
            <td v-if="redisId.mastername"> {{redisId.mastername}}</td>
            <td v-if="redisId.password">{{redisId.password}}</td>
            <td>{{redisId.createtime | formatDate}}</td>
            <td class="center aligned">
              <a title="连接" @click="connentredis(redisId.id)">
                <i class="sign in alternate icon"></i>
              </a>
            </td>
            <td class="center aligned">
              <a title="编辑" @click="modifyredis(redisId.id)">
                <i class="edit outline icon"></i>
              </a>
            </td>
            <td class="center aligned">
              <a title="删除" @click="removeredis(redisId.id)">
                <i class="minus square outline icon"></i>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
      <textarea v-show="isshow" v-model.trim="message"></textarea></br>
      <div v-show="isshow" class="ui fluid input">
        <input class="input_command" ref="input" type="text" v-model.trim="command" @keyup.enter="sendmeg()">
      </div>
      <div v-show="isshow" class="basic segment">
        <button class="ui primary basic button" @click="sendmeg()">Send</button>
        <button  class="ui negative basic button" @click="closeconnect()">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import redisid from '~/components/navbar.vue'
import axios from 'axios';
const  padDate = function(value) {
  return value < 10 ? '0' + value: value;
};
export default {
  data() {
    return {
      op: '',
      url: '',
      placeholder: 'IP地址:端口\nIP地址:端口',
      redisId: {},
      isActive: '',
      rdsname: '',
      rdstype: '',
      rdslist: '',
      rdsmastername: '',
      rdspwd: '',
      rdsprdname: '',
      usertoken: '',
      message: '',
      command: '',
      wssock: '',
      isshow:false,
      descshow: false,
    }
  },
  methods: {
    logout: function () {
      window.localStorage.removeItem('usertoken')
      window.location.href='./login'
    },
    removeredis: function (id) {
      let msg = "您真的确定要删除吗？\n\n请确认！"
      if (confirm(msg)==true) {
        axios.delete("http://127.0.0.1:8000/api/redislist/" + id, {headers: {'Authorization':"Bearer "+ this.usertoken}})
        .then(res => {
          alert("删除成功");
          this.rdsname= ''
          this.rdstype = ''
          this.rdslist = ''
          this.rdspwd = ''
          this.rdsmastername = ''
          this.rdsprdname = ''
          this.isActive = ''
          // 调用子组件navbar.vue中的getRedisList方法
          this.$refs.redisid.getRedisList();
          this.redisId = {}
        })
        .catch(err => {console.log("close error");})
      }
    },
    submitredis: function () {
      let op = this.op
      let url = this.url
      let data = {}
      if (this.rdsname.length > 0 && this.rdstype.length > 0 && this.rdslist.length > 0 && this.rdsprdname.length > 0) {
        if ( this.rdstype == "Sentinel" && this.rdsmastername.length == 0) {
          alert("请输入master name信息")
        } else {
          data['redisname'] = this.rdsname
          data['redistype'] = this.rdstype
          data['nodelist'] = this.rdslist.replace(/\n/g, ',');
          data['password'] = this.rdspwd
          data['mastername'] = this.rdsmastername
          data['projectname'] = this.rdsprdname
          if (op=="POST") {
            axios.post(url, data, {headers: {'Authorization':"Bearer "+ this.usertoken}})
            .then(res => {
              alert("添加成功")
              this.rdsname= ''
              this.rdstype = ''
              this.rdslist = ''
              this.rdspwd = ''
              this.rdsmastername = ''
              this.rdsprdname = ''
              this.isActive = ''
              this.$refs.redisid.getRedisList();
              this.redisId = {}
            })
            .catch(err => {console.log("create error");})
          } else if (op=="PUT") {
            axios.put(url, data, {headers: {'Authorization':"Bearer "+ this.usertoken}})
            .then(res => {
              alert("修改成功")
              this.isActive = ''
              this.redisId.redisname = this.rdsname
              this.redisId.redistype = this.rdstype
              this.redisId.nodelist = this.rdslist.replace(/\n/g, ',')
              this.redisId.password = this.rdspwd
              this.redisId.mastername = this.rdsmastername
              this.redisId.projectname = this.rdsprdname
            })
            .catch(err => {console.log("create error");})
          }
        }
      } else {
        alert("请输入redis信息")
      }
    },
    modifyredis: function (id) {
      this.rdsname = this.redisId.redisname
      this.rdstype = this.redisId.redistype
      this.rdslist = this.redisId.nodelist.replace(/,/g, '\n')
      this.rdspwd = this.redisId.password
      this.rdsmastername = this.redisId.mastername
      this.rdsprdname = this.redisId.projectname
      this.isActive = 'active'
      this.op = "PUT"
      this.url = "http://127.0.0.1:8000/api/redislist/" + id
    },
    connentredis: function (id) {
      const _this = this
      this.isshow = true
      this.wssock = new WebSocket("ws://127.0.0.1:8000/redis/client/?" + id);
      this.wssock.onopen = function () {
      }
      this.wssock.onmessage = function (evt)
      {
         const received_msg = JSON.parse(evt.data);
         if (typeof(received_msg.message)=="object"){
           Object.keys(received_msg.message).map(item=> {
              _this.message = _this.message + `${item}: ${JSON.stringify(received_msg.message[item])}` + '\n'
            })
         } else {
           _this.message = received_msg.message
         }
      };
      // 1.给input设置ref
      // 2.通过this.$refs获取dom
      // 3.给dom设置焦点focus()
      // this.$nextTick()将回调延迟到下次 DOM 更新循环之后执行
      // Tips: focus()在dom渲染之前执行是无效的(显示但不会获取焦点),所以的用$nextTick,
      this.$nextTick(function(){
        this.$refs.input.focus();
      })
      console.log(this.$refs.input);
    },
    sendmeg: function () {
      this.message = ''
      let commandlist = this.command.split(' ');
      let cmd = {}
      for (let i=0;i<commandlist.length;i++) {
        cmd["cmd" + i] = commandlist[i]
      }
      this.wssock.send(JSON.stringify(cmd))
      this.command = ''
    },
    closeconnect: function () {
      this.wssock.send(JSON.stringify({"cmd0": "close"}))
      this.isshow = false
    },
  },
  components: {
    "redisid" :redisid,
  },
  filters: {
    formatDate: function (value) {
        let date = new Date(value);
        let year = date.getFullYear();
        let month = padDate(date.getMonth() + 1);
        let day = padDate(date.getDate());
        let hours = padDate(date.getHours());
        let minutes = padDate(date.getMinutes());
        let seconds = padDate(date.getSeconds());
        return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes;
    },
  },
  watch: {
  },
  mounted: function () {
  },
}

</script>
<style lang="css" scoped>
.ui.basic.segment {
  margin-left: 98px;
  margin-right: -12px;
  padding-top:5px;
}
.ui.borderless.menu {
  height: 40px;
  box-shadow: 0 0 0 0;
}
.right.menu > .item {
  padding-right: 50px;
}
.ui.borderless.fixed.menu {
   background-color: rgb(24, 85, 105)
}
.inline.fields > .field {
  width:150px;
}

.ui.form .fields .field input  {
  width:450px;
}

.ui.form .fields .field textarea  {
  width:450px;
}

.ui.form .fields .field select  {
  width:450px;
}

.button.field {
  width:450px;
  margin-left: 150px;
  margin-right: 150px;
}
.right.menu .item {
  color: white;
}
textarea {
  width: 100%;
  height: 500px;
}
.basic.segment {
  padding-top: 10px;
}
.ui.pointing.red.basic.label {
  margin-top: -15px;
}
.center.aligned a {
  cursor: pointer;
}
</style>
