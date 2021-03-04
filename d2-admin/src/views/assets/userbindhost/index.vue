<template>
  <d2-container type="card">
    <template slot="header">主机绑定</template>
    <div class="handle-head">
      <el-row :gutter="20">
        <el-col :span="6"><div class="grid-content bg-purple">
          <el-button type="primary" size="mini" round @click="dialogVisibleCreate = true">创建绑定</el-button>
        </div>
        </el-col>
      </el-row>
      <host-list :values="host" :loading="loading" @edit="handleUpdate" @update="handleUpdateHost" @editGroup="handleUpdateGroup" @delete="handleDelete"></host-list>
    </div>
    <el-dialog
        :visible.sync="dialogVisibleCreate"
        title="创建"
        width="50%">
      <host-form ref="hostCreateForm"  @submit="handleSubmitCreate" @cancel="handleCreateCancel"></host-form>
    </el-dialog>
    <el-dialog
        :visible.sync="dialogVisibleUpdate"
        title="修改"
        width="50%">
      <host-form :form="detailForm"  @submit="handleSubmitUpdate" @cancel="handleUpdateCancel"></host-form>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogVisibleGroup"
      title="更改用户组"
      width="50%">
      <update-hgroup :form="detailForm" :glist.sync="groupList" :goption="groupOption" @submit="handleSubmitUpdateHostGroup" @cancel="handleGroupCancel"></update-hgroup>
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
import  { updatehost2group,gethostgroup,update_hostinfo,adduserbindhost,getuserbindhost, deleteuserbindhost,updateuserbindhost} from '@api/assets'
import HostForm from './host-form'
import HostList from './host-list'
import UpdateHgroup from './update-hostgroup'

export default {
name: "userbindhost",
components:{HostForm,HostList,UpdateHgroup} ,
mounted(){
    this.getUserBindHostData();
  },
data(){
  return {
    groupList: [],
    groupOption: [],
    dialogVisibleCreate: false,
    dialogVisibleUpdate: false,
    dialogVisibleGroup: false,
    host:[],
    detailForm: {
    },
    loading: true,
    total:0,
    getParams:{
      page:1,
      page_size:10,
    },
  }
} ,
methods:{
  getUserBindHostData(){
    getuserbindhost(this.getParams).then(res=>{
      this.host = res.results;
      this.total = res.count
      this.loading = false
    }).catch(function (error){
      console.log(error);
      this.$message({
        type: 'error',
        message: error.response.data.detail
      })
    })
  },
  handleCurrentChange(page){
    this.getParams.page=page
    this.getUserBindHostData()
  },
  handleSizeChange(size){
    this.getParams.page_size = size
    this.getUserBindHostData()
  },
  handleUpdateGroup(value){
    this.groupList = []
    this.detailForm = value
    this.dialogVisibleGroup = true
    gethostgroup().then(
      // 获取所有用户组列表
      res => {
        this.groupOption = res.results
      }
    )
    this.groupList = value.host_group.map(item => item.id)
  },
  handleSubmitUpdateHostGroup(id, value) {
    // 更新用户属组事件
    updatehost2group(id, value).then(
      () => {
        this.dialogVisibleGroup = false
        this.getUserBindHostData()
        this.$message({
          type: 'success',
          message: '更新成功'
        })
      },
      error => {
        this.$message({
          type: 'error',
          message: error.response.data.detail
        })
      }
    )
  },
  handleUpdate(value) {
    // 更新用户弹框显示
    this.dialogVisibleUpdate = true
        this.detailForm = value

  },
  handleUpdateHost(id){
    update_hostinfo(id).then((res)=>{
      this.$message({
        message:'恭喜你，更新主机信息成功',
        type:'success'
      })
    })
  },
  handleDelete(id) {
    deleteuserbindhost(id).then(
        () => {
          if (this.total % this.getParams.page_size === 1) {
            this.getParams.page = this.getParams.page - 1
          }
          this.getUserBindHostData()
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
    // 创建
    adduserbindhost(value).then(
        () => {
          this.getUserBindHostData()
          this.$refs.hostCreateForm.$refs.form.resetFields()
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
    // 更新
    updateuserbindhost(value).then(
        () => {
          this.dialogVisibleUpdate = false
          this.getUserBindHostData()
          this.$message({
            type: 'success',
            message: '更新成功'
          })
        },
        error => {
          this.$message({
            type: 'error',
            message: error.response.data.detail
          })
        })
  },
  handleCreateCancel() {
    // 创建取消按钮
    this.dialogVisibleCreate = false
    this.getUserBindHostData()
  },
  handleGroupCancel() {
    // 更新属组取消按钮
    this.dialogVisibleGroup = false
    this.getUserBindHostData()
  },
  handleUpdateCancel() {
    // 更新取消按钮
    this.dialogVisibleUpdate = false
    this.getUserBindHostData()
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
