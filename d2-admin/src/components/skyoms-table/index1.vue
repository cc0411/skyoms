<template>
  <div class="handle-head">
    <div class="filter">
      <el-select v-model="getParams.filtername" filterable class="d2-mr-5" size="mini"  placeholder="请选择数据中心"  @change="getData">
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
      <el-input v-model="getParams.search" placeholder="请输入集群名"  class="handle-input mr5" size="mini"  ></el-input>
      <el-button icon="el-icon-search"  size="mini" circle @click="getData" style="margin-left: 10px"></el-button>
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
<div class="table-template">
  <el-table
  id="table"
  ref="table"
  :data="tableData"
  style="width: 100%"
  @sort-change="changeTableSort"
  @selection-change="handleSelectionChange"
  >
  <el-table-column
  v-if="index"
  width="55"
  type="index"
  label="ID"
  align="center"
  >
  </el-table-column>
   <el-table-column
   v-if="tableOption.mutiSelect"
   width="55"
   type="selection"
   align="center"
   >
   </el-table-column>
    <el-table-column
    v-for="(item,index) in tableColumns"
    :key="index"
    :label="item.label"
    :prop="item.prop"
    :width="item.width"
    :fixed="item.fixed"
    :sortable="item.sort"
    v-if="item.istrue"
    align="center"
    show-overflow-tooltip
    >
      <template slot-scope="scope">
        <span v-if="item.render">{{item.render(scope.row)}}</span>
        <span v-else>{{scope.row[item.prop]}}</span>
      </template>
    </el-table-column>
    <el-table-column
      v-if="tableHandle.label"
      :width="tableHandle.width"
      :label="tableHandle.label"
      align="center"
      class-name="small-padding fixed-width"
    >
      <template slot-scope="scope">
        <template v-for="(item,index) in tableHandle.options">
          <el-tooltip
            class="item btn-xs"
            placement="top"
            effect="dark"
            :key="index"
            :content="item.label"
          >
            <el-button
              type="text"
              size="mini"
              :icon="item.icon"
              :disabled="item.disabled"
              @click.native.prevent="item.method(index,scope.row)"
            >{{item.label}}</el-button>
          </el-tooltip>
        </template>
      </template>
    </el-table-column>

  </el-table>

</div>
  <div class="d2-crud-footer">
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
  </div>
</template>

<script>
import Vue from 'vue'
import pluginExport from '@d2-projects/vue-table-export'
Vue.use(pluginExport)
export default {
  props: {
  index:{
      type:Boolean,
      default:()=>{return false;}
    },
  selection:{
      type:Boolean,
      default:()=>{return false;}
    },
  treeData:{
    type:Array,
    default:()=>{return [];}
  },
  colOptions:{
    type:Array,
    default:()=>{return [];}
  },
  colSelect:{
    type:Array,
    default:()=>{return [];}
  },
  tableData: {
    type:Array,
    default:()=>{return [];}
  },
  tableColumns: {
    type:Array,
    default:()=>{return [];}
  },
  total:{
    type:number,
    default:()=>{return 0;}
  },
  getParams:{
    type:Object,
    default:() =>{
      return {
        page:1,
        page_size:10,
        search:'',
        ordering:'',
        filtername: '',
      }
    }
  },
  tableHandle: {
    type: Object,
    default: () => {
      return {};
    }
  },
  tableOption: {
    type: Object,
    // eslint-disable-next-line vue/require-valid-default-prop
    default: {
      stripe: false, // 是否为斑马纹 table
      highlightCurrentRow: false, // 是否要高亮当前行
      border: false
    }
  } // table 表格的控制参数

},
  comments:{},
  created () {
  for (let i = 0; i < this.tableColumns.length; i++) {
    this.colSelect.push(this.tableColumns[i].label);
    this.colOptions.push(this.tableColumns[i].label);
  }
},
  watch: {
    colOptions(valArr){
      var that = this;
      var arr = that.colSelect.filter(i=>valArr.indexOf(i)<0);
      that.tableColumns.filter(i=>{
        if (arr.indexOf(i.label) !== -1){
          i.istrue=false;
        }else {
          i.istrue = true;
        }
      });
      this.$nextTick(() => {
        this.$refs.table.doLayout();

      });
    }
  },
  methods: {
  handleSelectionChange (val) {
    this.multipleSelection = val;
    this.$emit('handleSelectionChange', val);
  },
  exportExcel () {
    this.$export.excel({
      title : 'table列表',
      columns: this.tableColumns,
      data: this.tableData,
    }).then(() => {
      this.$message('表格导出成功')
    })
  },
  refreshClick(){
    this.getParams = {
      page:1,
      page_size:10,
      search:'',
      ordering:'',
      filtername: ''
    };
    this.getData()
  },
  handleCurrentChange(val){
    this.$emit('handleCurrentChange',Number(val))
  },
  handleSizeChange(val){
    this.$emit('handleSizeChange',Number(val))
  },
  changeTableSort(column){
    this.$emit('changeTableSort',column)
  },
  handleNodeClick(data){
    this.$emit('handleNodeClick',data.label)
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
