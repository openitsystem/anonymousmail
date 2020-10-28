<template>
  <div>
    <el-container>
        <el-header class="downLoadLine" style="padding:0px 0px 0px 0px">
          <el-row style="height:48px;white-space: nowrap;">
              <div @click="goBack()" style="display:inline-block;padding:13px 5px 13px 5px" class="blackColor classSpancursorpointer">
                <i class="el-icon-back" style="color: #7c6c5c;margin-left:5px;"></i>
                <span style="font-size:14px;color:#777">返回</span>
              </div>
          </el-row>
        </el-header>
        <el-main style="padding:0px;overflow:auto !important;height:calc(100Vh - 48px);">
          <el-row style="height:40px;white-space: nowrap;">
              <div @click="mailHeadersShow = !mailHeadersShow" style="display:inline-block;padding:10px 5px 9px 5px" class="blackColor classSpancursorpointer">
                <i class="el-icon-tickets" style="font-size:115%;color: #7c6c5c;margin-left:5px;"></i>
                <span style="font-size:14px;">邮件头</span>
              </div>
              <!-- <div style="display:inline-block;padding:10px 5px 9px 5px" class="blackColor classSpancursorpointer">
                <i class="el-icon-delete" style="font-size:115%;color: #0078d4;margin-left:5px;"></i>
                <span style="font-size:14px;">删除</span>
              </div> -->
          </el-row>
          <el-row style="margin:0px 30px 5px 30px;padding:10px 0px 10px 0px;" class="mailRowClass" v-show="mailHeadersShow">
            <el-col :span="24" style="padding:10px 0px 0px 0px;">
                <el-table :data="mailMessage.headers" style="width: 100%" size="mini">
                    <el-table-column prop="name" label="key" width="180"></el-table-column>
                    <el-table-column prop="value" label="value"></el-table-column>
                </el-table>
            </el-col>
          </el-row>
          <el-row style="margin:0px 30px 5px 30px;padding:10px 0px 10px 0px;" class="mailRowClass">
            <el-col :span="4" style="width:70px;padding:10px 0px 0px 0px;">
              <span>主题</span>
            </el-col>
            <el-col :span="20" style="padding:10px 0px 0px 0px;">
              <span>{{mailMessage.subject}}</span>
            </el-col>
          </el-row>
          <el-row style="margin:0px 30px 5px 30px;padding:10px 0px 10px 0px;" class="mailRowClass">
            <el-col :span="4" style="width:70px;padding:10px 0px 0px 0px;">
              <span>发件人</span>
            </el-col>
            <el-col :span="20" style="padding:10px 0px 0px 0px;">
              <span>{{mailMessage.from}}</span>
            </el-col>
          </el-row>
          <el-row v-show="mailMessage.attachments.length !==0 " style="margin:0px 30px 5px 30px;padding:10px 0px 10px 0px;" class="mailRowClass">
            <el-col :span="4" style="width:70px;padding:10px 0px 0px 0px;">
              <span>附件</span>
            </el-col>
            <el-col :span="20">
              <el-button @click="jumpattachment(item.id)" type="text" v-for="item in mailMessage.attachments" :key="item.id">{{item.name}}</el-button>
            </el-col>
          </el-row>
          <el-row style="margin:0px 30px 5px 30px;padding:10px 0px 0px 0px;">
            <el-col :span="24">
              <div class="grid-content bg-purple-dark" v-dompurify-html="mailMessage.body">
              </div>
            </el-col>
          </el-row>
        </el-main>
    </el-container>
  </div>
</template>
<style>
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
      background-color: #d5ecfe !important;
    }
  .mailRowClass {
    border-bottom: 1px solid #dcdcdc;
    font-size:14px
  }
</style>

<script>

import axios from 'axios'
import {getEmailsStorage,removeEmailsStorage,removeAllEmailsStorage} from '@/js/readMailList'
axios.defaults.withCredentials = true
export default {
  data () {
    return {
      uid:'',
      tableData:[],
      mailHeadersShow:false,
      mailMessage:{
        body:"",
        attachments:[],
        from:"",
        subject:"",
        headers:[],
      },
    }
  },
  async created(){
    await this.createdmethods()
  },
  watch:{
    async $route(){
      await this.createdmethods()
      await this.getMail()
    }
  },
  methods:{
    jumpattachment(attachmentid){
      window.open(this.serviceurl()+"/getmailattachment?uid="+this.uid+"&attachmentid="+attachmentid);
    },
    async createdmethods(){
      if (this.$route.params.num){
        this.uid = this.$route.params.num
        this.getMail()
      }
    },
    async getMail(){
      let that = this
      let loadingInstance = that.$loading();
      await axios
        .get(this.serviceurl() + '/getmailmessage/?uid=' + this.uid)
        .then(response => {
          that.mailMessage.body = response.data.results.body
          that.mailMessage.attachments = response.data.results.attachment
          that.mailMessage.subject = response.data.results.subject
          that.mailMessage.from = response.data.results.from
          that.mailMessage.headers = []
          Object.keys(response.data.results.headers).forEach(key => {
            that.mailMessage.headers.push({"name":key,"value":response.data.results.headers[key]})
          })
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
    async goBack(){
      this.$router.go(-1);
    },
    async removeEmails(){
      let loadingInstance = this.$loading();
      await removeEmailsStorage(this.uid)
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
