<template>
  <d2-container type="card">
    <template slot="header">主机组</template>
    <div class="handle-head">
      <el-row :gutter="20">
        <el-col :span="6"><div class="grid-content bg-purple">
          <el-button type="primary" size="mini" round @click="handleAdd">创建主机组</el-button>
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
    label="组名"
    width="110"
    ></el-table-column>
    <el-table-column
    prop="desc"
    label="描述"
    width="300">
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
    <groupdialog
    :dialog="dialog"
    :rowdata="rowdata"
    :FormData="FormData"
    @updategroup="getGroupData">
    </groupdialog>
  </d2-container>
</template>

<script>
import {gethostgroup,deletehostgroup} from '@api/assets'
import Groupdialog from '@/views/assets/hostgroup/Groupdialog'
export default {
name: 'HostGroup',
  components: { Groupdialog },
  mounted () {
  this.getGroupData()
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
      desc:''
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
  getGroupData(){
    gethostgroup(this.getParams).then(res=>{
      this.TableData = res.results;
      this.total = res.count
    }).catch(function (error){
      console.log(error)
    })
  },
  handleDelete(row){
    this.$confirm("确定删除吗？").then(()=>{
      deletehostgroup(row.id).then((res)=>{
        this.$message({
          message:'恭喜你，删除成功',
          type:'success'
        })
        this.getGroupData()
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
      desc:row.desc
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
    this.getGroupData()
  },
  handleSizeChange(size){
    this.getParams.page_size = size
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
