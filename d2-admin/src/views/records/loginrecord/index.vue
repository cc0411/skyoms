<template>
  <d2-container type="card">
    <template slot="header">登陆日志</template>
    <el-table
      :data="table.data"
      style="width: 100%"
      v-show="table.data.length>0"
    >
      <el-table-column
        v-for="(item,index) in table.columns"
        :key="index"
        :prop="item.prop"
        :label="item.label"
        :width="item.width"
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
import { getloginrecord } from '@api/records'
export default {

name: 'loginrecord',
mounted () {
  this.getLoginRecord()
},
data(){
  return {
    table:{
      columns:[
        {label:'用户',prop:'user',width:'120'},
        {label:'IP',prop:'ip',width:'200'},
        {label:'时间',prop:'login_time',width:'200'},
        {label:'方式',prop:'action',width:'120'},
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
} ,
methods: {
  getLoginRecord(){
    getloginrecord (this.table.getParams).then(res=>{
      this.table.data = res.results;
      this.table.total = res.count;
    }).catch(function (error){
      console.log(error)
    })
  },
  handleCurrentChange(page){
    this.table.getParams.page=page
    this.getLoginRecord();
  },
  handleSizeChange(size){
    this.table.getParams.page_size = size
    this.getLoginRecord();
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
