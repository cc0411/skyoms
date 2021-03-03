<template>
<div class='remotehostlist'>
  <el-table
    v-loading="loading"
    :data="values"
    v-if="values.length>0"
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
        <template slot-scope="scope">
          <div  slot="referehce" class="name-wapper" style="text-align: left">
          <el-tag :type="TYPE_CHOICES[scope.row.type].type">
            {{TYPE_CHOICES[scope.row.type].name}}
          </el-tag>
          </div>
        </template>

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
</div>
</template>

<script>
import update_hostinfo from "@api/assets";

export default {
name: "HostList",
props:{
  values: {
    type:Array,
    default: function (){
      return []
    }
  },
  loading: {
    type:Boolean,
    default: false
  }
},
data(){
  return {
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
  handleSelectionChange(val) {
    this.multipleSelection = val;
    console.log(this.multipleSelection)
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
    this.$confirm(`此操作将删除该${row.ip}主机绑定记录, 是否继续?`, '删除主机绑定', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      this.$emit('delete', row.id)
    }).catch(() => {
      this.$message({
        type: 'info',
        message: '已取消删除'
      })
    })
  },
  handleEdit(row){
    this.$emit('edit', row)
  },

}
}
</script>

<style scoped>

</style>
