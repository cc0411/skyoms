<template>
  <div class="form">
    <el-form ref="form" :model="form" :rules="rules" label-width="150px" label-position='left' class="host-form">
      <el-form-item label="主机名" prop="hostname">
        <el-input v-model="form.hostname"></el-input>
        <span class="error-text" v-if="hosterror">{{hosterror}}</span>
      </el-form-item>
      <el-form-item label="类型" prop="type">
        <el-select v-model="form.type" placeholder="请选择设备类型">
          <el-option v-for="item in TYPE_CHOICES" :key="item.key" :label="item.name"
                     :value="item.key"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="IP地址" prop="ip">
        <el-input v-model="form.ip"></el-input>
        <span class="error-text" v-if="iperror">{{iperror}}</span>
      </el-form-item>
      <el-form-item label="协议" prop="protocol">
        <el-select v-model="form.protocol" placeholder="请选择协议">
          <el-option v-for="item in PROTOCOL_CHOICES" :key="item.key" :label="item.name"
                     :value="item.key"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="环境" prop="env">
        <el-select v-model="form.env" placeholder="请选择环境">
          <el-option v-for="item in ENV_CHOICES" :key="item.key" :label="item.name"
                     :value="item.key"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="端口" prop="port">
        <el-input v-model="form.port"></el-input>
        <span class="error-text" v-if="porterror">{{porterror}}</span>
      </el-form-item>
      <el-form-item label="系统" prop="release">
        <el-input v-model="form.release"></el-input>
      </el-form-item>
      <el-form-item label="平台" prop="platform">
        <el-select v-model="form.platform" placeholder="请选择协议">
          <el-option v-for="item in PLATFORM_CHOICES" :key="item.key" :label="item.name"
                     :value="item.key"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="远程用户" prop="remote_user">
        <el-select v-model="form.remote_user" filterable placeholder="请选择用户">
          <el-option  v-for="item in RemoteUserData" :key="item.name" :value="item.name" :label="item.name"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="rdp验证方式" prop="security">
        <el-input v-model="form.security"></el-input>
      </el-form-item>
      <el-form-item label="是否启用" prop="enabled">
        <el-switch v-model="form.enabled"  active-color="#13ce66"
                   inactive-color="#ff4949"></el-switch>
      </el-form-item>
      <el-form-item>
        <el-form-item class="button-right">
          <p class="error-text" v-show="error">{{error}}</p>
          <el-button size="small" type="primary" @click="submitForm">提交</el-button>
          <el-button size="small" @click="cancelForm">取消</el-button>
        </el-form-item>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {gethostgroup,getremoteuser} from '@/api/assets'
export default {
  name: "HostForm",
  mounted() {
    this.getGroupData();
    this.getRemoteUserData();
  },
  props:{
    form: {
      type:Object,
      default: function (){
        return {
          hostname :'',
          type:'',
          ip:'',
          protocol:'',
          env:'',
          port:22,
          release:'',
          platform:'',
          remote_user:'',
          security:'',
          enabled:true,
        }
      }
    },
  },
  data() {
    return {
      GroupData: {},
      RemoteUserData:{},
      PROTOCOL_CHOICES: [
        {key: 1, name: 'ssh'},
        {key: 2, name: 'rdp'},
        {key: 3, name: 'vnc'},
        {key: 4, name: 'telnet'},
      ],
      TYPE_CHOICES: [
        {key: 1, name: '服务器'},
        {key: 2, name: '交换机'},
        {key: 3, name: '虚拟机'},
      ],
      ENV_CHOICES: [
        {key:1,name:'product'},
        {key:2,name:'dev'}
      ],
      PLATFORM_CHOICES:[
        {key:1,name:'linux'},
        {key:2,name:'windows'},
        {key:3,name: 'other'}
      ],
      error: false,
      hosterror: false,
      iperror: false,
      porterror: false,
      rules: {
        hostname: [
          {required: true, message: '主机名不能为空', trigger: 'blur'}
        ],
      }
    }
  },
  methods: {
    //编辑和添加功能具体实现
    submitForm()  {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$emit('submit', this.form)
        }
        else {
          this.$message.error('失败了！');
          return false
        }
      })
    },
    cancelForm() {
      this.$emit('cancel')
    },
    getRemoteUserData(){
      getremoteuser().then(res=>{
        console.log(res)
        this.RemoteUserData = res.results
      }).catch(function (error){
        console.log(error)
      })
    },
    getGroupData() {
      gethostgroup()
        .then(res => {
          this.GroupData = res.results;
        }).catch(function (error) {
        console.log(error)
      })
    },

  }


}
</script>

<style scoped>
.host-form {
  position: relative;
  display: block
}
.button-right {
  text-align: right;
}
</style>
