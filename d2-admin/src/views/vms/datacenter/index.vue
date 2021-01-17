<template>
  <d2-container type="card">
    <template slot="header">数据中心</template>
    <div class="download">
      <el-button type="primary" size="mini" round @click="exportExcel">
        <d2-icon name="download"/>导出Excel
      </el-button>
      <el-popover placement="top-end" width="50" trigger="click" style="margin-left: 5px">
        <el-checkbox-group v-model="colOptions">
          <el-checkbox v-for="item in colSelect" :label="item" :key="item"></el-checkbox>
        </el-checkbox-group>
        <el-button slot="reference" type="info" size="mini"  circle icon="el-icon-setting"></el-button>
      </el-popover>
    </div>
    <el-table
      ref="datacenterTable"
      :data="table.data"
      style="width: 100%"
      v-show="table.data.length>0"
      @sort-change="changeTableSort"
    >
      <el-table-column
        v-for="(item,index) in table.columns"
        :key="index"
        :sortable=item.sort
        :prop="item.prop"
        :label="item.label"
        :width="item.width"
        v-if="item.istrue"
      align="center">
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
import Vue from 'vue'
import pluginExport from '@d2-projects/vue-table-export'
Vue.use(pluginExport)
import { getdatacenter } from '@api/vms'
export default {
name: 'datacenter',
  mounted () {
    this.getDatacenterData();
    for (let i = 0; i < this.table.columns.length; i++) {
      this.colSelect.push(this.table.columns[i].label);
      this.colOptions.push(this.table.columns[i].label);
    }
  },
  watch: {
    colOptions(valArr){
      var that = this;
      var arr = that.colSelect.filter(i=>valArr.indexOf(i)<0);
      that.table.columns.filter(i=>{
        if (arr.indexOf(i.label) !== -1){
          i.istrue=false;
        }else {
          i.istrue = true;
        }
      });
      this.$nextTick(() => {
        this.$refs.datacenterTable.doLayout();

      });
    }
  },
  data() {
    return {
      colOptions: [],
      colSelect: [],
      table: {
        columns:[
          //{label:'ID',prop:'id'},
          {label:'数据中心',prop:'name',width:'150',sort:false,istrue: true},
          {label:'CPU总计/Ghz',prop:'cputotal',width:'130',sort:false,istrue: true},
          {label:'CPU使用量/Ghz',prop:'cpuusage',width:'130',sort:false,istrue: true},
          {label:'内存总计/G',prop:'memtotal',width:'130',sort:false,istrue: true},
          {label:'内存使用量/G',prop:'memusage',width:'130',sort:false,istrue: true},
          {label:'存储总计/T',prop:'datatotal',width:'130',sort:false,istrue: true},
          {label:'存储剩余量/T',prop:'datafree',width:'130',sort:"custom",istrue: true},
          {label:'宿主机数量',prop:'numhosts',width:'130',sort:"custom",istrue: true},
          {label:'虚拟机数量',prop:'vmscount',width:'130',sort:"custom",istrue: true},
          {label:'CPU总核数',prop:'numcpuscores',width:'110',sort:false,istrue: true},

        ],
        data : [],
        size: 'mini',
        stripe: 'true',
        fit:'true',
        getParams:{
          page:1,
          page_size:10,
          ordering:''
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
        title: '数据中心列表'
      }).then(()=>{
        this.$message('表格导出成功')
      })
    },
    //获取数据中心信息
    getDatacenterData() {
      getdatacenter(this.table.getParams).then(res=>{
        this.table.data = res.results;
        this.table.total = res.count;
      }).catch(function (error){
        console.log(error)
      })
    },
    handleCurrentChange(page){
      this.table.getParams.page=page
      this.getDatacenterData()
    },
    handleSizeChange(size){
      this.table.getParams.page_size = size
      this.getDatacenterData()
    },
    //对指定字段排序
    changeTableSort (column) {
      //  获取字段名和排序类型
      var fieldName = column.prop;
      var sortingType = column.order;
      //按照降序排序
      if (sortingType === "descending") {
        this.table.getParams.ordering = '-' + fieldName
        this.getDatacenterData()
        // this.table.data = this.table.data.sort((a, b) => b[fieldName] - a[fieldName]);
      }
      //按照升序排序
      else {
        this.table.getParams.ordering = fieldName
        this.getDatacenterData()
        //this.table.data = this.table.data.sort((a, b) => a[fieldName] - b[fieldName]);

      }
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

