<template>
    <el-row>
        <el-col style="width:300px" :span="12">
            <el-container>
                <el-header class="downLoadLine">
                    <div class="sidebar-header">
                        <div class="brand-container">
                            <a href="/" class="brand">
                                <i class="el-icon-connection"></i>
                                mfk.app
                            </a>
                        </div>
                    </div>
                </el-header>
                <el-main class="mainleft" style="background-color:#fafafa;padding: 0 0 0 0;">
                    <el-menu :default-active="activeIndex" router background-color="#fafafa" active-text-color="black" style="width:calc(100Vw-48px)">
                        <el-menu-item index="/addEmailBox" class="downLoadLine">
                            <i class="el-icon-plus" style="color:#7c6c5c;"></i>
                            <span slot="title">添加邮箱</span>
                        </el-menu-item>
                        <el-menu-item index="/emailList/all">
                            <i class="el-icon-s-home" style="color:#7c6c5c;"></i>
                            <span slot="title">全部邮箱</span>
                        </el-menu-item>
                        <el-menu-item :index="menuItemIndex + i" v-for="i in mailaddressList" :key="i">
                            <span slot="title" style="margin-left:23px;">{{i}}</span>
                        </el-menu-item>
                    </el-menu>
                </el-main>
            </el-container>
        </el-col>
        <el-col style="width:calc(100Vw - 300px);" :span="12">
            <router-view @removeMailListMessage='removeMailListMessage'></router-view>
        </el-col>
    </el-row>
</template>
<style>
  .el-header {
    height: 48px !important;
  }
  .downLoadLine {
    border-bottom: 1px solid #dcdcdc;
    background-color: #fff;
  }
  .mainleft {
    height: calc(100vh - 48px) !important;
    border-right: 1px solid #dcdcdc;
  }
  .brand {
    font-size: 20px;
    color: #7c6c5c;
    text-decoration: none;
  }
  .brand-container {
    padding: 10px 0 10px 14px;
}
.el-menu-item{
    padding: .7em 1em !important;
    line-height: 20px !important;
    height: 40px !important;
}
.el-menu-item.is-active {
      background-color: #DCDCDC !important;
    }
.el-menu-item:hover{
  background: #DCDCDC !important;
}
.blackColor:hover{
  background: #f0f0f0 !important;
}
.classSpancursorpointer{
  cursor: pointer;
}
</style>
<script>

import axios from 'axios'
axios.defaults.withCredentials = true
import {getEmailsStorage,removeEmailsStorage} from '@/js/readMailList'
export default {
  data () {
    return {
      mailaddressList:[],
      menuItemIndex:"/emailList/",
      mailaddress:"",
      activeIndex:"",
    }
  },
  created(){
    this.getMailListMessage()
  },
  watch:{
    async $route(){
      await this.getMailListMessage()
    }
  },
  methods:{
    async getMailListMessage(){
      let getEmailsStorageValue = getEmailsStorage()
      this.mailaddressList = getEmailsStorageValue.mailList
      this.activeIndex = this.$route.path
    },
    async removeMailListMessage(){
      this.mailaddressList = []
    },
    async getMailList(){
      let that = this
      that.tableData = []
      await axios
        .get(this.serviceurl() + '/getmaillist/?address=' + that.mailaddress)
        .then(response => {
          that.tableData = response.data.results
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
