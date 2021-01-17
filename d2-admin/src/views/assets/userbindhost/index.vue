<template>
  <d2-container type="card">
    <template slot="header">主机绑定</template>
    <div class="handle-head">
      <el-row :gutter="20">
        <el-col :span="6"><div class="grid-content bg-purple">
          <el-button type="primary" size="mini" round @click="handleAdd">创建绑定</el-button>
        </div>
        </el-col>
      </el-row>
    </div>
    <el-table
      :data="TableData"
      v-if="TableData.length>0"
      style="width: 100%"
      @selection-change="handleSelectionChange">
      <el-table-column
        type="selection"
        width="55">
      </el-table-column>
      <el-table-column
        prop="remote_user"
        label="用户"
        width="110"
      ></el-table-column>
      <el-table-column
        prop="hostname"
        label="主机名"
        width="110">
      </el-table-column>
      <el-table-column
      prop="type"
      label="类型"
      width="110">
        <div  slot="referehce" class="name-wapper" style="text-align: left">
      <template slot-scope="scope">
        <el-tag :type="TYPE_CHOICES[scope.row.type].type">
          {{TYPE_CHOICES[scope.row.type].name}}
        </el-tag>
      </template>
        </div>
      </el-table-column>
      <el-table-column
        prop="ip"
        label="IP"
        width="110">
      </el-table-column>
      <el-table-column
        prop="protocol"
        label="协议"
        width="110">
        <template slot-scope="scope">
          <div  slot="referehce" class="name-wapper" style="text-align: left">
          <el-tag :type="PROTOCOL_CHOICES[scope.row.protocol].type">
            {{PROTOCOL_CHOICES[scope.row.protocol].name}}
          </el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="env"
        label="环境"
        width="110">
        <template slot-scope="scope">
          <div  slot="referehce" class="name-wapper" style="text-align: left">
          <el-tag :type="ENV_CHOICES[scope.row.env].type">
            {{ENV_CHOICES[scope.row.env].name}}
          </el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="port"
        label="端口"
        width="110">
      </el-table-column>
      <el-table-column
        prop="release"
        label="系统"
        width="110">
      </el-table-column>
      <el-table-column
        prop="platform"
        label="平台"
        width="110">
        <template slot-scope="scope">
          <div  slot="referehce" class="name-wapper" style="text-align: left">
          <el-tag :type="PLATFORM_CHOICES[scope.row.platform].type">
            {{PLATFORM_CHOICES[scope.row.platform].name}}
          </el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="security"
        label="RDP验证方式"
        width="110">
      </el-table-column>
      <el-table-column
        prop="enabled"
        label="是否启用"
        width="110">
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
        prop="host_group"
        label="主机组"
        width="110">
        <template slot-scope="scope">
          <div v-for="(item, index) in scope.row.host_group" :key="index" style="float:left">
            <el-tag style="margin-right: 3px" size="mini" >{{ item.name }}</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="300"
        align="center"
        fixed="right"
      >
        <template slot-scope="scope">
          <el-button  size="mini" @click="handleUpdate(scope.row)" >更新</el-button>
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
    <userbindhostdialog
      :dialog="dialog"
      :rowdata="rowdata"
      :FormData="FormData"
      @updatebindhosts="getUserBindHostData">
    </userbindhostdialog>
  </d2-container>
</template>

<script>
import { getuserbindhost, deleteuserbindhost,update_hostinfo} from '@api/assets'
import userbindhostdialog from '@/views/assets/userbindhost/userbindhostdialog'


export default {
name: 'userbindhost',
components:{
  userbindhostdialog
},
mounted(){
  this.getUserBindHostData();
},
data(){
  return {
    multipleSelection:[],
    TableData:[],
    dialog:{
      show:false,
      title:'',
      option:'edit',
    },
    FormData:{
      hostname:'',
      type:'',
      ip:'',
      protocol:'',
      env:'',
      port:'',
      release:'',
      platform:'',
      remote_user:'',
      security:'',
      enabled:true,
    },
    rowdata:{},
    total:0,
    getParams:{
      page:1,
      page_size:10,
    },
    PROTOCOL_CHOICES: {
     1: {type: 'success', name: 'ssh'},
    2:{type: 'info', name: 'rdp'},
    3:{type: 'warning', name: 'vnc'},
    4:{type: '', name: 'telnet'},
    },
    TYPE_CHOICES: {
      1:{type: 'success', name: '服务器'},
      2:{type: 'info', name: '交换机'},
      3:{type: 'warning', name: '虚拟机'},
    },

    ENV_CHOICES: {
      1:{type:'success',name:'product'},
      2:{type:'danger',name:'dev'}
    },
    PLATFORM_CHOICES:{
     1: {type:'success',name:'linux'},
     2: {type:'warning',name:'windows'},
     3:{type:'info',name:'other'}
    },

  }
},
  methods:{
    getUserBindHostData(){
      getuserbindhost(this.getParams).then(res=>{
        console.log(res)
        this.TableData = res.results;
        this.total = res.count
      }).catch(function (error){
        console.log(error)
      })
    },
    handleUpdate(row){
      update_hostinfo({id:row.id}).then((res)=>{
        this.$message({
          message:'恭喜你，更新主机信息成功',
          type:'success'
        })
      })

    },
    handleDelete(row){
      this.$confirm("确定删除吗？").then(()=>{
        deleteuserbindhost(row.id).then((res)=>{
          this.$message({
            message:'恭喜你，删除成功',
            type:'success'
          })
          this.getUserBindHostData()
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
        hostname:row.hostname,
        type:row.type,
        ip:row.ip,
        protocol:row.protocol,
        env:row.env,
        port:row.port,
        release:row.release,
        platform:row.platform,
        remote_user:row.remote_user,
        security:row.security,
        enabled:row.enabled,
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
      this.getUserBindHostData()
    },
    handleSizeChange(size){
      this.getParams.page_size = size
      this.getUserBindHostData()
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
      console.log(this.multipleSelection)
    }

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
