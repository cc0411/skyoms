<template>
  <div class="remoteuserdialog">
    <el-dialog
      :title="dialog.title"
      :visible.sync="dialog.show"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :modal-append-to-body="false">
      <div class="form">
        <el-form ref="remoteuserform" :model="FormData" :rules="rules" label-width="80px">
          <el-form-item label="名称" prop="name">
            <el-input v-model="FormData.name"></el-input>
          </el-form-item>
          <el-form-item label="用户名" prop="username">
            <el-input v-model="FormData.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="FormData.password"></el-input>
          </el-form-item>
          <el-form-item label="是否可以su" prop="enabled">
            <el-switch v-model="FormData.enabled"  active-color="#13ce66"
                       inactive-color="#ff4949"></el-switch>
          </el-form-item>
          <el-form-item label="超级用户" prop="superuser">
            <el-input v-model="FormData.superuser"></el-input>
          </el-form-item>
          <el-form-item label="特权密码" prop="superpass">
            <el-input v-model="FormData.superpass"></el-input>
          </el-form-item>
          <p class="error-text" v-show="error">{{error}}</p>
          <el-form-item>
            <el-button type="primary" @click="onSubmit('remoteuserform')">提交</el-button>
            <el-button @click="dialog.show=false">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {addremoteuser,updateremoteuser} from '@/api/assets'

export default {
  name: 'remoteuserdialog',
  props:{
    dialog:Object,
    FormData:Object,
    rowdata:Object
  },
  data(){
    return {
      error:false,
      rules:{
        name:[
          {required:true,message:'名称不可以为空',trigger:'blur'},
          {max:32,message: '最大不能超过32个字符',trigger: 'blur'}
        ],
        username:[
          {required:true,message:'用户名不可以为空',trigger:'blur'},
        ],
        password:[
          {required:true,message:'密码不可以为空',trigger:'blur'},
        ],
      }

    }
  } ,
  methods: {
    onSubmit(Formname){
      var that= this
      this.$refs[Formname].validate((valid)=>{
        if(valid){
          const option = this.dialog.option ==="add" ?addremoteuser(this.FormData):updateremoteuser(this.rowdata.id,this.FormData);
          option.then(res=>{
            this.$message.success('添加或更新成功')
            this.dialog.show = false;
            this.$emit('updateremoteuser')
          }).catch(function (error){
            const err = error.response.data;
            if("non_field_errors" in err){
              that.error = err.non_field_errors[0];

            }
            if("name" in err){
              that.error = err.name[0];
            }
            if("username" in err){
              that.error = err.username[0];
            }
            if("password" in err){
              that.error = err.password[0];
            }

          })

        }
        else {
          this.$message.error('失败了');
        }


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

