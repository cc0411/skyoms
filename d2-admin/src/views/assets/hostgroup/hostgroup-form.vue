<template>
  <div class="form">
    <el-form ref="form" :model="form" :rules="rules" label-width="80px" class="group-form">
      <el-form-item label="组名" prop="name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input type="textarea" rows="5" v-model="form.desc"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button size="small" type="primary" @click="submitForm">提交</el-button>
        <el-button size="small" @click="cancelForm">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "hostgroup-form",
  props: {
    form: {
      type: Object,
      default: function() {
        return {
          name: '',
          desc:''
        }
      }
    }
    },
  data() {
    return {
      rules: {
        name: [
          { required: true, message: '请输入组名', trigger: 'blur' },
          { max: 32, message: '长度不能超过32个字符', trigger: 'blur' }
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
          return false
        }
      })
    },
    cancelForm() {
      this.$emit('cancel')
    }
  }

}
</script>

<style scoped>
.group-form {
  position: relative;
  display: block
}
.button-right {
  text-align: right;
}
</style>
