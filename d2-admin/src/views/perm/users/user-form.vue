<template>
  <div>
    <el-form ref="form" :model="form" :rules="rules" label-width="100px" class="user-form">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" placeholder="请输入姓名"></el-input>
      </el-form-item>
      <el-form-item label="邮箱地址" prop="email">
        <el-input v-model="form.email" placeholder="请输入email"></el-input>
      </el-form-item>
      <el-form-item label="手机" prop="mobile">
        <el-input v-model="form.mobile" placeholder="请输入手机号"></el-input>
      </el-form-item>
      <el-form-item class="button-right">
        <el-button size="small" @click="cancelForm">取消</el-button>
        <el-button size="small" type="primary" @click="submitForm">{{ value }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
name: 'UserForm',
props: {
  form: {
    type:Object,
    default: function (){
      return {
        username :'',
        password:'',
        name:'',
        email:'',
        mobile:'',

      }
    }
  },
  value:{
    type:String,
    required:true,

  },
},
  data(){
    return {
      rules: {
        username:[
          {required: true,message:'请输入用户名',trigger:'blur'},
          {max:64,message:'长度不要超过64个字符',trigger: 'blur'}
          ],
        name:[
          {max:32,message:'长度不要超过32个字符',trigger:'blur'}
        ],
        email:[
          {type:'email',message:'请输入正确的邮箱格式',trigger:'blur'}
        ],
        mobile:[
          {max:11,message:'长度不要超过11位',trigger:'blur'}
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$emit('submit', this.form)
        } else {
          console.log('error')
          return false;
        }
      })
    },
    cancelForm() {
      this.$emit('cancel')
    }

  }



}
</script>

<style lang="scss" scoped>
.user-form {
  position: relative;
  display: block
}
.button-right {
  text-align: right;
}
</style>
