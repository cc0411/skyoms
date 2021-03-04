<template>
  <d2-container type="card">
    <template slot="header">批量命令</template>
   <el-form :model="FormData" ref="cmdform" :rules="rules" label-width="100px" label-position='left'>
     <el-form-item label="主机组" prop="hostgroup">
       <el-select v-model="FormData.hostgroup" placeholder="请选择主机组">
         <el-option v-for="item in HostGroupData" :key="item.value" :label="item.label" :value="item.value" ></el-option>
       </el-select>
       <span class="error-text" v-if="grouperror">{{grouperror}}</span>
     </el-form-item>
     <el-form-item label="主机" prop="host">
        <el-select v-model="FormData.host" filterable multiple  placeholder="请选择主机">
          <el-option v-for="item in  HostData" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
       <span class="error-text" v-if="hosterror">{{hosterror}}</span>
     </el-form-item>
     <el-form-item label="命令" prop="cmd">
       <el-input v-model="FormData.cmd"></el-input>
       <span class="error-text" v-if="cmderror">{{cmderror}}</span>
     </el-form-item>
     <el-form-item>
       <p class="error-text" v-show="error">{{error}}</p>
       <el-button type="primary" @click="onSubmit('cmdform')">执行命令</el-button>
     </el-form-item>
   </el-form>



  </d2-container>
</template>

<script>
import {getselecthostgroup} from '@api/batch'
export default {
name: 'cmd',
mounted () {
  this.GetSelectHostgroupData();
},
  data(){
 return {
   FormData:{
     hostgroup:[],
     host:[],
     cmd:''
   },
   HostData:[],
   HostGroupData:[],
   hosterror:false,
   grouperror:false,
   cmderror:false,
   error:false,
   rules:{
     hostgroup:[
       {required:true,trigger:'blue',message:'请选择主机组'}
       ],
     host:[
       {required:true,trigger:'blue',message:'请选择主机'}
     ],
     cmd:[
       {required:true,trigger:'blue',message:'请输入命令'}
     ]
   }

 }
},
methods:{
  onSubmit(Formname) {

  },
  GetSelectHostgroupData(){
    getselecthostgroup().then(res=>{
      this.HostGroupData = res
    }).catch(function (error){
      console.log(error)
    })


  }
}
}
</script>

<style scoped>

</style>
