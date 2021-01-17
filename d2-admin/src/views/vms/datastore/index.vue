<template>
  <d2-container type="card">
    <template slot="header">存储</template>
    <div class="handle-head">
      <div class="filter">
        <el-select v-model="table.getParams.datacenter__name" filterable class="d2-mr-5" size="mini"  placeholder="请选择数据中心"  @change="getDatastoreData">
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
        <el-input v-model="table.getParams.search" placeholder="请输入存储名"  class="handle-input mr5" size="mini"  ></el-input>
        <el-button icon="el-icon-search"  size="mini" circle @click="getDatastoreData" style="margin-left: 10px"></el-button>
        <el-button size="mini"  icon="el-icon-refresh" circle @click="refreshClick"></el-button>
      </div>
      <div class="download">
        <el-button type="primary" size="mini" round @click="exportExcel">
          <d2-icon name="download"/>导出Excel
        </el-button>
      </div>
    </div>
    <el-table
      :data="table.data"
      style="width: 100%"
      @sort-change="changeTableSort"
      v-if="table.data.length>0"
    >
      <el-table-column
        v-for="(item,index) in table.columns"
        :sortable=item.sort
        :key="index"
        :prop="item.prop"
        :label="item.label"
        :width="item.width"
        show-overflow-tooltip>
        <template slot-scope="scope">
          <div v-if="(item.prop==='rate')" slot="referehce" class="name-wapper">
            <el-progress :percentage="scope.row.rate" :text-inside="true" :stroke-width="15" :color="customColorMethod"></el-progress>
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
import Vue from 'vue'
import { getdatastore } from '@api/vms'
import {createNamespacedHelpers} from 'vuex'
const {mapState} = createNamespacedHelpers('d2admin')
import pluginExport from '@d2-projects/vue-table-export'
Vue.use(pluginExport)
export default {
name: 'datastore',
  mounted () {
    this.getDatastoreData();
    this.$store.dispatch('d2admin/fetTreeData')
  },
  computed:{
    ...mapState({
      treeData: state=>state.vm.treeData
    })
  },
  data() {
    return {
      table: {
        columns:[
          //{label:'ID',prop:'id',sort:'custom'},
          {label:'存储名',prop:'name',sort:false},
          {label: '数据中心',prop: 'datacenter',sort: false},
          {label:'存储总计/T',prop:'capacity',sort: false},
          {label:'存储剩余量/T',prop:'freespace',sort: 'custom'},
          {label: '剩余率/%',prop:'rate',sort: false,width:'300'}

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

      }
    }
  },
  methods: {
    //导出excel
    exportExcel() {
      this.$export.excel({
        columns: this.table.columns,
        data: this.table.data,
        title: '存储列表'
      }).then(()=>{
        this.$message('表格导出成功')
      })
    },
    //获取集群信息
    getDatastoreData() {
      getdatastore(this.table.getParams).then(res=>{
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
      this.getDatastoreData();
    },
    handleCurrentChange(page){
      this.table.getParams.page=page
      this.getDatastoreData();
    },
    handleSizeChange(size){
      this.table.getParams.page_size = size
      this.getDatastoreData();
    },
    //对指定字段排序
    changeTableSort (column) {
      //  获取字段名和排序类型
      var fieldName = column.prop;
      var sortingType = column.order;
      //按照降序排序
      if (sortingType === "descending") {
        this.table.getParams.ordering = '-' + fieldName
        this.getDatastoreData();
        // this.table.data = this.table.data.sort((a, b) => b[fieldName] - a[fieldName]);
      }
      //按照升序排序
      else {
        this.table.getParams.ordering = fieldName
        this.getDatastoreData();
        //this.table.data = this.table.data.sort((a, b) => a[fieldName] - b[fieldName]);

      }
    },
    customColorMethod(size){
      if(size<30){
        return '#EE0000';
      }
      else if(size<60){
        return '#EEC900';
      }
      else{
        return '#00EE00';
      }

    }
  }
}
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
&:last-child {
   margin-bottom: 0;
 }
}
.el-col {
  border-radius: 4px;
}
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
