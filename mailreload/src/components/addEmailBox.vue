<template>
  <div>
    <el-container>
        <el-header class="downLoadLine" style="padding:0px 0px 0px 0px">
        </el-header>
        <el-main style="padding:0px;overflow:auto !important;height:calc(100Vh - 48px);" class="classFontFamily">
            <el-row style="margin:0px 0px 5px 30px;padding:10px 0px 0px 0px;">
              <el-col :span="3">
                 <div>&nbsp;</div>
              </el-col>
              <el-col :span="21" style="margin-top:30px;font-size:18px">
                <div class="grid-content bg-purple-dark" style="margin-top:10px">
                  添加邮箱
                </div>
                <div class="grid-content bg-purple-dark" style="margin-top:20px">
                  <el-input placeholder="请输入内容" v-model="input2" class="inpurWidth" autofocus size="small">
                    <template slot="append">@mfk.app</template>
                  </el-input>
                </div>
                <div class="grid-content bg-purple-dark" style="margin-top:20px">
                  <el-button type="primary" class="btnprimary" size="small" @click="addmailaddress">添加</el-button>
                </div>
              </el-col>
            </el-row>
        </el-main>
    </el-container>
  </div>
</template>

<style>
.inpurWidth{
  width: 350px !important;
}
  .classFontFamily{
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",SimSun,sans-serif !important;
  }
  .btnprimary {
    color: #fff !important;
    background-color: #7c6c5c !important;
    border-color: #7c6c5c !important;
}
  .btnprimary:hover {
    background-color: #615344 !important;
}
</style>

<script>

import axios from 'axios'
axios.defaults.withCredentials = true
import {generateMixed,addEmailsStorage} from '@/js/readMailList'
export default {
  data () {
    return {
      input2:"",
    }
  },
  created(){
    this.creatMailAddress()
  },
  methods:{
    async creatMailAddress(){
      this.input2 =  generateMixed(5)
    },
    async addmailaddress(){
      addEmailsStorage(this.input2)
      this.$message({
        message: '添加成功',
        type: 'success',
        duration:'600'
      });
      this.$router.push({path:'/emailList/'+this.input2+"@mfk.app"})
    },
  },
}
</script>

<style scoped>
</style>
