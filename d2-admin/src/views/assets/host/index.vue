<template>
  <d2-container type="card">
    <template slot="header">主机</template>
    <div class="handle-head">
      <el-row :gutter="20">
        <el-col :span="6"><div class="grid-content bg-purple">
          <el-button type="primary" size="mini" round @click="handleAdd">创建主机</el-button>
        </div>
        </el-col>
      </el-row>
    </div>
    <el-table
      :data="TableData"
      v-if="TableData.length>0"
      style="width: 100%"
      >
      <el-table-column
        prop="server"
        label="IP"
        width="110"
      ></el-table-column>
      <el-table-column
        prop="cpu_number"
        label="物理CPU数"
        width="110">
      </el-table-column>
      <el-table-column
        prop="vcpu_number"
        label="逻辑CPU数"
        width="110">
      </el-table-column>
      <el-table-column
        prop="memory"
        label="内存/G"
        width="110">
      </el-table-column>
      <el-table-column
        prop="disk"
        label="硬盘/G"
        width="120">
      </el-table-column>
      <el-table-column
        prop="server_model"
        label="型号"
        width="110">
      </el-table-column>
      <el-table-column
        label="操作"
        width="300"
        align="center"
        fixed="right"
      >
        <template slot-scope="scope">
          <el-button  size="mini" @click="handlehostinfo(scope.row)" >查看</el-button>
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
    <hostdialog
      :dialog="dialog"
      :rowdata="rowdata"
      :FormData="FormData"
      @updatehost="getHostData">
    </hostdialog>
  </d2-container>
</template>

<script>
import {gethost,deletehost} from '@api/assets'
import hostdialog from '@/views/assets/host/hostdialog'
export default {
  name: 'host',
  components: { hostdialog },
  mounted () {
    this.getHostData()
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
        server:'',
        cpu_number:0,
        vcpu_number:0,
        cpu_info:'',
        os:'',
        os_kernel:'',
        memory:'',
        disk:'',
        filesystems:'',
        interfaces:'',
        server_model:'',

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
    getHostData(){
      gethost(this.getParams).then(res=>{
        console.log(res)
        this.TableData = res.results;
        this.total = res.count
      }).catch(function (error){
        console.log(error)
      })
    },
    handlehostinfo(row){
      this.$router.push('/assets/host/' +row.id+"/")
},
    handleDelete(row){
      this.$confirm("确定删除吗？").then(()=>{
        deletehost(row.id).then((res)=>{
          this.$message({
            message:'恭喜你，删除成功',
            type:'success'
          })
          this.getHostData()
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
        server:row.server,
        cpu_number:row.cpu_number,
        vcpu_number:row.vcpu_number,
        cpu_info:row.cpu_info,
        os:row.os,
        os_kernel:row.os_kernel,
        memory:row.memory,
        disk:row.disk,
        filesystems:row.filesystems,
        interfaces:row.interfaces,
        server_model:row.server_model,
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
      this.getHostData()
    },
    handleSizeChange(size){
      this.getParams.page_size = size
      this.getHostData()
    },



  }

}
</script>

<style scoped>
.pagination ,.el-pagination{
  text-align: center;
  margin-top: 10px;
}

</style>
