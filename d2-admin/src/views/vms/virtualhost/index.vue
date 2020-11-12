<template>
  <d2-container type="card">
    <template slot="header">虚拟机</template>
    <div class="handle-head">
      <div class="filter">
        <el-select v-model="table.getParams.datacenter__name" filterable class="d2-mr-5" size="mini"  placeholder="请选择数据中心"  @change="getVirtualhostData">
          <el-option
            v-for="item in treeData"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </div>
      <div class="search" >
        <el-input v-model="table.getParams.search" placeholder="请输入虚拟机名称"  class="handle-input mr5" size="mini"  ></el-input>
        <el-button icon="el-icon-search"  size="mini" circle @click="getVirtualhostData" style="margin-left: 10px"></el-button>
        <el-button size="mini"  icon="el-icon-refresh" circle @click="refreshClick"></el-button>
      </div>
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
    </div>
    <el-table
      ref="virtualTable"
      :data="table.data"
      style="width: 100%"
      @sort-change="changeTableSort"
      v-show="table.data.length>0"
    >
      <el-table-column
        v-for="(item,index) in table.columns"
        :key="index"
        :sortable=item.sort
        :prop="item.prop"
        :label="item.label"
        :width="item.width"
        v-if="item.istrue"
        >
        <template slot-scope="scope">
          <div v-if="(item.prop==='status')" slot="referehce" class="name-wapper" style="text-align: left">
            <el-tag style="color: #000" :color="VIRTUAL_STATUS[scope.row[item.prop]].color">
              {{VIRTUAL_STATUS[scope.row[item.prop]].type}}
            </el-tag>
          </div>
          <div v-else-if="(item.prop==='powerState')" slot="referehce" class="name-wapper" style="text-align: left">
            <el-tag style="color: #000" :color="POWER_STATE[scope.row[item.prop]].color">
              {{POWER_STATE[scope.row[item.prop]].type}}
            </el-tag>
          </div>
          <span v-else>{{scope.row[item.prop]}}</span>
        </template>
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
import { getvirtualhost } from '@api/vms'
import Vue from 'vue'
import pluginExport from '@d2-projects/vue-table-export'
import {createNamespacedHelpers} from 'vuex'
const {mapState} = createNamespacedHelpers('d2admin')
Vue.use(pluginExport)
export default {
  name: 'virtualhost',
  created () {
    this.getVirtualhostData();
    this.$store.dispatch('d2admin/fetTreeData')
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
        this.$refs.virtualTable.doLayout();

      });
    }
  },
  computed:{
    ...mapState({
      treeData: state=>state.vm.treeData
    })
  },
  data() {
    return {
      colOptions: [],
      colSelect: [],
      table: {
        columns:[
          //{label:'ID',prop:'id',sort:"custom",},
          {label:'虚拟机名',prop:'name',sort:false,width:300,istrue: true},
          {label:'数据中心',prop:'datacenter',sort:false,width:150,istrue: true},
          {label:'宿主机',prop:'host',sort:false,width:130,istrue: true},
          {label: 'IP',prop: 'ip',sort: false,width:130,istrue: true},
          {label:'电源状态',prop:'powerState',sort:false,width:110,istrue: true},
          {label:'CPU核数',prop:'cpunums',sort:false,width:110,istrue: true},
          {label:'内存/G',prop:'memtotal',sort:'custom',width:110,istrue: true},
          {label:'系统',prop:'os',sort:false,width:300,istrue: true},
          {label:'CPU用量/Mhz',prop:'cpuusage',sort:false,width:130,istrue: true},
          {label:'内存用量/M',prop:'memusage',sort:false,width:130,istrue: true},
          {label:'存储用量/G',prop:'store_usage',sort:'custom',width:130,istrue: true},
          {label: '状态',prop: 'status',sort: false,width:120,istrue: true}
        ],
        data : [],
        size: 'mini',
        stripe: 'true',
        fit:'true',
        getParams:{
          page:1,
          page_size:10,
          search:'',
          ordering:'',
          datacenter__name: ''
        },
        total:0,
      },
      VIRTUAL_STATUS: {
        'green' :{'color':'#67C23A','type':'正常'},
        'yellow' :{'color':'#E6A23C','type':'异常'}
      },
      POWER_STATE: {
        'poweredOn':{'color':'#67C23A',type:'已开机'},
        'poweredOff':{'color':'#E6A23C',type:"已关机"}
      }
    }
  },
  methods: {
    //导出excel
    exportExcel() {
      this.$export.excel({
        columns: this.table.columns,
        data: this.table.data,
        title: '虚拟机列表'
      }).then(()=>{
        this.$message('表格导出成功')
      })
    },
    //获取所以虚拟机信息
    getVirtualhostData() {
      getvirtualhost (this.table.getParams).then(res=>{
        this.table.data = res.results;
        this.table.total = res.count;
      }).catch(function (error){
        console.log(error)
      })
    },
    refreshClick(){
      this.table.getParams = {
        page:1,
        page_size:10,
        search:'',
        ordering:'',
        datacenter__name: ''
      };
      this.getVirtualhostData();
    },
    handleCurrentChange(page){
      this.table.getParams.page=page
      this.getVirtualhostData();
    },
    handleSizeChange(size){
      this.table.getParams.page_size = size
      this.getVirtualhostData();
    },
    //对指定字段排序
    changeTableSort (column) {
      //  获取字段名和排序类型
      var fieldName = column.prop;
      var sortingType = column.order;
      //按照降序排序
      if (sortingType === "descending") {
        this.table.getParams.ordering = '-' + fieldName
        this.getVirtualhostData();
        // this.table.data = this.table.data.sort((a, b) => b[fieldName] - a[fieldName]);
      }
      //按照升序排序
      else {
        this.table.getParams.ordering = fieldName
        this.getVirtualhostData();
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
.pagination {
  float: right;
  margin-top: 20px;
}
.search {
  float: left;
}
.filter {
  float: left;
  margin-right: 10px;
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
