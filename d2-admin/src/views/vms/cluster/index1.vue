<template>
  <d2-container type="card">
    <template slot="header">集群</template>
    <TableCom
    :table-data="tableData"
    :table-label="tableColumns"
    :table-option="tableOption"
    :get-Params="getParams"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"

    ></TableCom>
  </d2-container>
</template>

<script>
import { getcluster} from '@api/vms'
import {createNamespacedHelpers} from 'vuex'
const {mapState} = createNamespacedHelpers('d2admin')
import TableCom from '@/components/skyoms-table/index'
const {tableColumns,sendThis} = require('./index')
export default {
name: 'cluster',
created () {
  this.getData()
},
  comments: {
  TableCom
},
computed:{
    ...mapState({
      treeData: state=>state.vm.treeData
    })
  },
data(){
  return {
    tableColumns:tableColumns,
    tableOption: {mutiSelect:false},
    tableData:[],
    total:0,
    getParams:{
      page:1,
      page_size:10,
      search:'',
      ordering:'',
      datacenter__name: ''
    }
  }
},
methods:{
  getData () {
    getcluster(this.getParams).then(res => {
      console.log(this.getParams)
      this.tableData = res.results;
      this.total = res.count;
      console.log(this.tableData)
    }).catch(function (error) {
      console.log(error)
    })
  },
  handleCurrentChange(page){
    this.getParams.page=page
    this.getData()
  },
  handleSizeChange(size){
    this.getParams.page_size = size
    this.getData()
  },
  //对指定字段排序
  changeTableSort (column) {
    console.log(column);
    //  获取字段名和排序类型
    var fieldName = column.prop;
    var sortingType = column.order;
    //按照降序排序
    if (sortingType === "descending") {
      this.getParams.ordering = '-' + fieldName
      this.getData()
      // this.table.data = this.table.data.sort((a, b) => b[fieldName] - a[fieldName]);
    }
    //按照升序排序
    else {
      this.getParams.ordering = fieldName
      this.getData()
      //this.table.data = this.table.data.sort((a, b) => a[fieldName] - b[fieldName]);
    }
  },

}
}
</script>

<style scoped>

</style>
