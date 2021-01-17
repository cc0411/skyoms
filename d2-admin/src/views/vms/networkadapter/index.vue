<template>
  <d2-container type="card">
    <template slot="header">网络</template>
    <div class="download">
      <el-button type="primary" size="mini" round @click="exportExcel">
        <d2-icon name="download"/>导出Excel
      </el-button>
    </div>
    <el-table
      :data="table.data"
      style="width: 100%"
      :default-sort = "{prop: 'id', order: 'descending'}"
      v-if="table.data.length>0"
    >
      <el-table-column
        v-for="(item,index) in table.columns"
        :key="index"
        :prop="item.prop"
        :label="item.label"
        :width="item.width"
        show-overflow-tooltip>
      </el-table-column>
    </el-table>
    <div class="d2-crud-footer">
      <div class="d2-crud-pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="table.getParams.page"
          :page-sizes="[10, 20, 50,100,500]"
          :page-size="table.getParams.page_size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="table.total">
        </el-pagination>
      </div>
    </div>
  </d2-container>
</template>

<script>
import { getnetworkadapter } from '@api/vms'
import Vue from 'vue'
import pluginExport from '@d2-projects/vue-table-export'
Vue.use(pluginExport)
export default {
name: 'networkadapter',
  mounted() {
    this.getNetworkadapterData();
  },
  data() {
    return {
      table: {
        columns:[
          //{label:'ID',prop:'id',width:80},
          {label:'网络名',prop:'name',width:300},
          {label: '数据中心',prop: 'datacenter',width: 180},
          {label:'Vlan',prop:'vlanid',width:100},
          {label:'类型',prop:'type',width:130},

        ],
        data : [],
        size: 'mini',
        stripe: 'true',
        fit:'true',
        getParams:{
          page:1,
          page_size:10,
        },
        total:0,

      }
    }
  },
  methods: {
    //导出excel
    exportExcel() {
      this.$export.excel({
        columns: this.table.columns,
        data: this.table.data,
        title: '网络列表'
      }).then(()=>{
        this.$message('表格导出成功')
      })
    },
    //获取网络信息
    getNetworkadapterData() {
      getnetworkadapter(this.table.getParams).then(res=>{
        this.table.data = res.results;
        this.table.total = res.count;
      }).catch(function (error){
        console.log(error)
      })
    },
    handleCurrentChange(page){
      this.table.getParams.page=page
      this.getNetworkadapterData()
    },
    handleSizeChange(size){
      this.table.getParams.page_size = size
      this.getNetworkadapterData()
    },
  }
}
</script>

<style scoped>
.handle-head {
  padding-bottom: 5px;
}
.pagination ,.el-pagination{
  text-align: center;
  margin-top: 10px;
}
.search {
  float: left;
}
.handle-input {
  width: 300px;
  display: inline-block;
}
.download {
  margin-top: 5px;
  margin-bottom: 5px;
  margin-inside: 5px;
  float: right;
}

</style>
