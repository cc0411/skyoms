<template>
  <d2-container type="card">
    <template slot="header">远程用户</template>
    <div class="handle-head">
      <el-row :gutter="20">
        <el-col :span="6"><div class="grid-content bg-purple">
          <el-button type="primary" size="mini" round @click="handleAdd">创建用户</el-button>
        </div>
        </el-col>
      </el-row>
    </div>
    <el-table
      :data="TableData"
      v-if="TableData.length>0"
      style="width: 100%">
      <el-table-column
        prop="name"
        label="名称"
        width="110"
      ></el-table-column>
      <el-table-column
        prop="username"
        label="用户名"
        width="110">
      </el-table-column>
      <el-table-column
        prop="enabled"
        label="是否可以su"
        width="110"
      >
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.enabled"
            active-color="#13ce66"
            inactive-color="#ff4949"
            disabled>
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column
        prop="superuser"
        label="超级用户"
        width="110">
      </el-table-column>
      <el-table-column
        label="操作"
        width="200"
        align="center"
      >
        <template slot-scope="scope">
          <el-button  size="mini" @click="handleEdit(scope.row)" >编辑</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
        </template>

      </el-table-column>
    </el-table>
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
    <remoteuserdialog
      :dialog="dialog"
      :rowdata="rowdata"
      :FormData="FormData"
      @updateremoteuser="getRemoteUserData">
    </remoteuserdialog>
  </d2-container>
</template>

<script>
import {getremoteuser,deleteremoteuser} from '@api/assets'
import remoteuserdialog from '@/views/assets/remoteuser/remoteuserdialog'
export default {
  name: 'HostGroup',
  components: { remoteuserdialog },
  mounted () {
    this.getRemoteUserData()
  },
  data(){
    return {
      TableData:[],
      dialog:{
        show:false,
        title:'',
        option:'edit',
      },
      FormData:{
        name:'',
        username:'',
        password:'',
        enabled:false,
        superuser:'',
        superpass:''
      },
      rowdata:{},
      total:0,
      getParams:{
        page:1,
        page_size:10,
      }
    }

  },
  methods:{
    getRemoteUserData(){
      getremoteuser(this.getParams).then(res=>{
        console.log(res)
        this.TableData = res.results;
        this.total = res.count
      }).catch(function (error){
        console.log(error)
      })
    },
    handleDelete(row){
      this.$confirm("确定删除吗？").then(()=>{
        deleteremoteuser(row.id).then((res)=>{
          this.$message({
            message:'恭喜你，删除成功',
            type:'success'
          })
          this.getRemoteUserData()
        })
      }).catch(error=>{
        this.$message.info('点错了')
        console.log('error')
      })
    },
    handleEdit(row){
      this.dialog={
        title:'编辑',
        show:true,
        option:'edit',
      }
      this.rowdata = row;
      this.FormData = {
        name:row.name,
        username: row.username,
        password: row.password,
        enabled:row.enabled,
        superuser:row.superuser,
        superpass:row.superpass
      }
    },
    handleAdd(){
      this.dialog = {
        title:'添加',
        show:true,
        option:'add'
      }
    },
    handleCurrentChange(page){
      this.getParams.page=page
      this.getRemoteUserData()
    },
    handleSizeChange(size){
      this.getParams.page_size = size
      this.getRemoteUserData()
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
