<template>
  <div class="hostdialog">
    <el-dialog
      :title="dialog.title"
      :visible.sync="dialog.show"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :modal-append-to-body="false">
      <div class="form">
        <el-form ref="hostform" :model="FormData" :rules="rules" label-width="120px">
          <el-form-item label="IP" prop="server">
            <el-select v-model="FormData.server" filterable placeholder="请选择主机">
              <el-option  v-for="item in RemoteUserData" :key="item.ip" :value="item.ip" :label="item.ip"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="物理CPU数" prop="cpu_number">
            <el-input v-model="FormData.cpu_number"></el-input>
          </el-form-item>
          <el-form-item label="逻辑CPU数" prop="vcpu_number">
            <el-input v-model="FormData.vcpu_number"></el-input>
          </el-form-item>
          <el-form-item label="CPU信息" prop="cpu_info">
            <el-input v-model="FormData.cpu_info"></el-input>
          </el-form-item>
          <el-form-item label="系统" prop="os">
            <el-input v-model="FormData.os"></el-input>
          </el-form-item>
          <el-form-item label="内核" prop="os_kernel">
            <el-input v-model="FormData.os_kernel"></el-input>
          </el-form-item>
          <el-form-item label="内存" prop="memory">
            <el-input v-model="FormData.memory"></el-input>
          </el-form-item>
          <el-form-item label="硬盘" prop="disk">
            <el-input v-model="FormData.disk"></el-input>
          </el-form-item>
          <el-form-item label="文件系统" prop="filesystems">
            <el-input v-model="FormData.filesystems"></el-input>
          </el-form-item>
          <el-form-item label="网卡" prop="interfaces">
            <el-input v-model="FormData.interfaces"></el-input>
          </el-form-item>
          <el-form-item label="型号" prop="server_model">
            <el-input v-model="FormData.server_model"></el-input>
          </el-form-item>
          <p class="error-text" v-show="error">{{error}}</p>
          <el-form-item>
            <el-button type="primary" @click="onSubmit('hostform')">提交</el-button>
            <el-button @click="dialog.show=false">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {addhost,updatehost,getuserbindhost} from '@/api/assets'

export default {
  name: 'hostdialog',
  props:{
    dialog:Object,
    FormData:Object,
    rowdata:Object
  },
  mounted () {
    this.GetRemoteUserData();
  },
  data(){
    return {
      RemoteUserData:{},
      error:false,
      rules:{}
    }
  } ,
  methods: {
    onSubmit(Formname){
      var that= this
      this.$refs[Formname].validate((valid)=>{
        if(valid){
          const option = this.dialog.option ==="add" ?addhost(this.FormData):updatehost(this.rowdata.id,this.FormData);
          option.then(res=>{
            this.$message.success('添加或更新成功')
            this.dialog.show = false;
            this.$emit('updatehost')
          }).catch(function (error){
            const err = error.response.data;
            if("non_field_errors" in err){
              that.error = err.non_field_errors[0];
            }
          })
        }
        else {
          this.$message.error('失败了');
        }


      })

    },
    GetRemoteUserData(){
      getuserbindhost().then(res=>{
        this.RemoteUserData = res.results
      }).catch(function (error){
        console.log(error)
      })
    }


  }
}
</script>

<style scoped>
.error-text {
  color:#fa8341;
}
</style>
