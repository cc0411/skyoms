<template>

  <div>
    <el-form ref="form" :model="form" label-width="100px" class="change-pass">
      <el-form-item v-if="is_superuser == false" label="旧密码" prop="old_password">
        <el-input v-model="form.old_password"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="new_password">
        <el-input v-model="form.new_password"></el-input>
      </el-form-item>

      <el-form-item class="button-right">
        <el-button size="small" @click="cancelForm">取消</el-button>
        <el-button size="small" type="primary" @click="submitForm">更新</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {createNamespacedHelpers} from 'vuex'
const {mapState} = createNamespacedHelpers('d2admin')
export default {
name: 'ChangePassword',
  props: {
    form: {
      type: Object,
      default: function() {
        return {
          old_password: '',
          new_password: ''
        }
      }
    }
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapState({
     is_superuser:state=>state.userinfo.is_superuser,
    })
  },
  methods: {
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$emit('submit', this.form.id, this.form)
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

</style>
