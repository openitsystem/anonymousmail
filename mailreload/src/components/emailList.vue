<template>
  <div>
    <el-container>
        <el-header class="downLoadLine" style="padding:0px 0px 0px 0px">
          <el-row style="height:48px;white-space: nowrap;">
              <div style="display:inline-block;padding:14px 5px 14px 5px;" class="blackColor classSpancursorpointer" v-if="mailaddress !== 'all'" v-clipboard:copy="mailaddress" v-clipboard:success="onCopy" v-clipboard:error="onError">
                <i class="el-icon-document-copy" style="margin-left:5px;;color:#777"></i>
                <span style="color: #7c6c5c;font-size:14px">{{mailaddress}}</span>
                <span style="font-size:14px;color:#777">复制</span>
              </div>
              <div @click="refulsh()" style="display:inline-block;padding:14px 5px 14px 5px" class="blackColor classSpancursorpointer">
                <i class="el-icon-refresh" style="color: #7c6c5c;margin-left:5px;"></i>
                <span style="font-size:14px;color:#777">刷新</span>
              </div>
              <div @click="removeEmails()" style="display:inline-block;padding:14px 5px 14px 5px" class="blackColor classSpancursorpointer" v-if="mailaddress !== 'all'">
                <i class="el-icon-delete" style="color: #7c6c5c;margin-left:5px;"></i>
                <span style="font-size:14px;color:#777">删除邮箱</span>
              </div>
              <div @click="removeAllEmails()" style="display:inline-block;padding:14px 5px 14px 5px" class="blackColor classSpancursorpointer" v-else>
                <i class="el-icon-delete" style="color: #7c6c5c;margin-left:5px;"></i>
                <span style="font-size:14px;color:#777">删除全部邮箱</span>
              </div>
          </el-row>
        </el-header>
        <el-main v-if="tableData.length !== 0" style="padding:0px;overflow:auto !important;height:calc(100Vh - 48px);">
          <div @click="jumpMessage(item.uid)" v-for="item in tableData" :key="item.uid" class="borderBottom classSpancursorpointer classFontFamily aa">
              <el-row style="margin:0px 0px 5px 30px;padding:10px 0px 0px 0px;">
                <el-col :span="24"><div class="grid-content bg-purple-dark">{{item.subject}}
                  <i class="el-icon-paperclip" style="color: #7c6c5c;margin-left:5px;font-size:14px" v-if="item.attachments !== 0"></i></div></el-col>
              </el-row>
              <el-row style="margin:0px 0px 10px 30px;">
                <el-col :span="8"><div class="grid-content bg-purple-dark">{{item.from}}</div></el-col>
                <el-col :span="16"><div class="grid-content bg-purple-dark">{{item.date}}</div></el-col>
              </el-row>
          </div>
          <footer class="ui-link">
            <a href="https://beian.miit.gov.cn/">苏 ICP 备 14002037号-3</a>
          </footer>
        </el-main>
        <el-main v-else style="padding:0px;overflow:auto !important;height:calc(100Vh - 48px);">
          <div >
              <el-row style="margin:0px 0px 5px 30px;padding:10px 0px 0px 0px;">
                <el-col :span="24"><div class="grid-content bg-purple-dark">
                  <img src="..\..\static\notFound.png" class="no-emails-found">
                </div>
                </el-col>
              </el-row>
              <el-row style="margin:0px 0px 10px 30px;">
                <el-col :span="24">
                  <div style="text-align: center;display: grid;margin-top: 15px">
                    <div style="margin: auto;max-width: 381px; padding: 0 20px">
                      <span class="ng-binding">还没有邮件哦。<br><br></span>
                      <span class="ng-binding" v-if="mailaddress == 'all'">不想暴露私人邮箱地址，你可以用这些去注册网站，保护你的真实邮箱。<br><br></span>
                      <span class="ng-binding" v-else>不想暴露私人邮箱地址，你可以用 <b class="ng-binding classSpancursorpointer" style="color: #0078d4;" v-clipboard:copy="mailaddress" v-clipboard:success="onCopy" v-clipboard:error="onError">{{mailaddress}}</b> 去注册网站，保护你的真实邮箱。<br><br></span>
                    </div>
                  </div>
                </el-col>
              </el-row>
          </div>
          <!-- https://blog.csdn.net/cuk5239/article/details/107699169 -->
          <InArticleAdsense
              data-ad-client="ca-pub-8245321006725365"
              data-ad-slot="1234567890">
          </InArticleAdsense>
          <footer class="ui-link">
            <a href="https://beian.miit.gov.cn/">苏 ICP 备 14002037号-3</a>
          </footer>
        </el-main>
    </el-container>
  </div>
</template>
<style>
.ui-link{
  font-size: 13px;
  bottom:0;
  position:absolute;
}
.no-emails-found {
    width: 45%;
    margin-left: 27%;
    margin-top: 15%;
}
  .borderBottom {
    border-bottom: 1px solid #dcdcdc;
    line-height:1;
    font-size:14px
  }
  .classSpancursorpointer{
    cursor: pointer;
  }
  .classFontFamily{
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",SimSun,sans-serif;
  }
.borderBottom:hover {
      background-color: #DCDCDC !important;
    }
</style>

<script>

import axios from 'axios'
import {getEmailsStorage,removeEmailsStorage,removeAllEmailsStorage} from '@/js/readMailList'
axios.defaults.withCredentials = true
export default {
  data () {
    return {
      mailaddress:'',
      tableData:[],
    }
  },
  async created(){
    if (this.$route.params.num){
      this.mailaddress = this.$route.params.num
    } else {
      this.mailaddress = "all"
    }
    this.getMailList()
  },
  watch:{
    async $route(){
      await this.createdmethods()
      await this.getMailList()
    }
  },
  mounted(){
    if (this.timer){
      clearInterval(this.timer)
    } else {
      this.timer = setInterval(async () => {
        let that = this
        await axios
          .get(this.serviceurl() + '/getmaillist/?address=' + this.mailaddress)
          .then(response => {
            if ((this.tableData).length < (response.data.results).length){
              this.tableData = response.data.results
              this.$message({
                message: '有新邮件请查收',
                type: 'success',
                duration:'800'
              });
            }
        })
      },11000)
    }
  },
  destroyed(){
    clearInterval(this.timer)
  },
  methods:{
    jumpMessage(uid){
      this.$router.push({path:'/email/'+uid})
    },
    async createdmethods(){
      await this.getMailListMessage()
      if (this.$route.params.num){
        this.mailaddress = this.$route.params.num
      } else {
        this.mailaddress = "all"
      }
    },
    async getMailListMessage(){
      let ccc = getEmailsStorage()
    },
    async getMailList(){
      let that = this
      that.tableData = []
      let loadingInstance = that.$loading();
      await axios
        .get(this.serviceurl() + '/getmaillist/?address=' + this.mailaddress)
        .then(response => {
          this.tableData = response.data.results
          loadingInstance.close();
        })
    },
    async handleEdit(index, row){
      let that = this
      await axios
        .get(this.serviceurl() + '/getmailmessage/?uid=' + row.uid)
        .then(response => {
          that.dialogFormVisible = true
          that.mailValue = response.data.results
        })
    },
    async refulsh(){
      let loadingInstance = this.$loading();
      await this.getMailList()
      loadingInstance.close();
      this.$message({
        message: '刷新成功',
        type: 'success',
        duration:'600'
      });
    },
    async removeEmails(){
      let loadingInstance = this.$loading();
      await removeEmailsStorage(this.mailaddress)
      loadingInstance.close();
      this.$message({
        message: '删除成功',
        type: 'success',
        duration:'600'
      });
      this.$router.push({path:'/emailList/all'})
    },
    async removeAllEmails(){
      let loadingInstance = this.$loading();
      (this.tableData).splice(0,this.tableData.length)
      await removeAllEmailsStorage()
      await this.$emit('removeMailListMessage')
      loadingInstance.close();
      this.$message({
        message: '全部删除成功',
        type: 'success',
        duration:'600'
      });
    },
    onCopy(e){
      this.$message({
        message: '复制成功，可以直接粘贴',
        type: 'success',
        duration:'600'
      });
    },
    onError(){
      this.$message({
        message: '复制失败，请手动复制',
        type: 'error',
        duration:'600'
      });
    },
  },
}
</script>

<style scoped>
</style>
