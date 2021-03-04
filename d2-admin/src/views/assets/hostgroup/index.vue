<template>
  <d2-container type="card">
    <template slot="header">主机组</template>
    <div class="handle-head">
      <el-row :gutter="20">
        <el-col :span="6"><div class="grid-content bg-purple">
          <el-button type="primary" size="mini" round @click="dialogVisibleCreate = true">创建主机组</el-button>
        </div>
        </el-col>
      </el-row>
    </div>
    <group-list :values="group" :loading="loading" @edit="handleUpdate"  @delete="handleDelete" @list="handlelistMember"></group-list>
    <el-dialog
      :visible.sync="dialogVisibleCreate"
      title="创建主机组"
      width="50%">
      <group-form ref="gform"  @submit="handleSubmitCreate" @cancel="handleCreateCancel"></group-form>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogVisibleUpdate"
      title="修改主机组信息"
      width="50%">
      <group-form :form="detailForm"  @submit="handleSubmitUpdate" @cancel="handleUpdateCancel"></group-form>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogVisibleHost"
      :title="groupname"
      width="50%">
      <group-member :values="member" @delete="handleDeleteGroupMember"></group-member>
    </el-dialog>
    <div class="d2-crud-pagination">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page.sync="getParams.page"
        :page-sizes="[10, 20, 50,100,500]"
        :page-size="getParams.page_size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </div>
  </d2-container>
</template>

<script>
import {gethostgroup,deletehostgroup,addhostgroup,updatehostgroup,deleteHostGroupMember} from '@api/assets'
import GroupList from './hostgroup-list'
import GroupForm from './hostgroup-form'
import GroupMember from './hostgroup-member'
export default {
name: 'HostGroup',
  components: { GroupList, GroupForm, GroupMember },
  mounted () {
  this.getGroupData()
},
data(){
  return {
    group: [],
    detailForm: {},
    loading: true,
    groupname: '',
    member: [],
    groupid: '',
    dialogVisibleCreate: false,
    dialogVisibleUpdate: false,
    dialogVisibleHost: false,
    total:0,
    getParams:{
      page:1,
      page_size:10,
    }
  }

},
methods:{
  getGroupData(){
    gethostgroup(this.getParams).then(res=>{
      this.group= res.results;
      this.total = res.count
      this.loading = false
    }).catch(function (error){
      console.log(error)
    })
  },
  handleUpdate(value){
    this.dialogVisibleUpdate = true
    this.detailForm = value
  },
  handlelistMember(value) {
    // 获取用户组成员列表
    this.groupname = value.name + '组成员列表'
    this.dialogVisibleHost = true
    this.member = value.hosts
    this.groupid = value.id
  },
  handleDelete(id){
    // 删除组
    deletehostgroup(id).then(
      () => {
        if (this.total % this.getParams.page_size === 1) {
          this.getParams.page = this.getParams.page - 1
        }
        this.getGroupData()
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      },
      err => {
        this.$message({
          type: 'error',
          message: err.response.data.detail
        })
      }
    )
  },
  handleSubmitCreate(value) {
    // 创建用户组
    addhostgroup(value).then(
      () => {
        this.getGroupData()
        this.$refs.gform.$refs.form.resetFields()
        this.dialogVisibleCreate = false
        this.$message({
          type: 'success',
          message: '创建成功'
        })
      },
      error => {
        this.$message({
          type: 'error',
          message: error.response
        })
      }
    )
  },
  handleSubmitUpdate(value) {
    // 编辑更新用户组
    updatehostgroup(value).then(
      () => {
        this.getGroupData()
        this.dialogVisibleUpdate = false
        this.$message({
          type: 'success',
          message: '更新成功'
        })
      },
      err => {
        this.$message({
          type: 'error',
          message: err.response.data.detail
        })
      })
  },
  handleDeleteGroupMember(value){
    deleteHostGroupMember(this.groupid, value).then(
      () => {
        this.dialogVisibleHost = false
        this.getGroupData()
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      },
      err => {
        this.$message({
          type: 'error',
          message: err.response.data.detail
        })
      }
    )
  },
  handleCurrentChange(page){
    this.getParams.page=page
    this.getGroupData()
  },
  handleSizeChange(size){
    this.getParams.page_size = size
    this.getGroupData()
  },
  handleCreateCancel() {
    // 对话框取消实现
    this.dialogVisibleCreate = false
    this.getGroupData()
  },
  handleUpdateCancel() {
    // 对话框取消实现
    this.dialogVisibleUpdate = false
    this.getGroupData()
  },

}

}
</script>

<style scoped>
.pagination ,.el-pagination{
  text-align: center;
  margin-top: 10px;
}
.handle-head {
  margin-top: 10px;
}
</style>
