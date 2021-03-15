<template>
  <d2-container type="card">
    <template slot="header">批量命令</template>
   <el-form :model="form" ref="form" :rules="rules" label-width="100px" label-position='left'>
     <el-form-item label="主机组" prop="hostgroup">
       <el-select v-model="form.hostgroup" placeholder="请选择主机组" @change="changeHostgroup">
         <el-option v-for="item in HostGroupData" :key="item.value" :label="item.label" :value="item.value" ></el-option>
       </el-select>
     </el-form-item>
     <el-form-item label="主机" prop="host">
        <el-select v-model="form.host" filterable multiple  placeholder="请选择主机">
          <el-option v-for="item in  HostData" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
     </el-form-item>
     <el-form-item label="命令" prop="cmd">
       <el-input v-model="form.cmd"></el-input>
     </el-form-item>
     <el-form-item>
       <el-button type="primary" @click="onSubmit">执行命令</el-button>
     </el-form-item>
   </el-form>

    <pre id="pre" style="width:100%;max-height:0px;background-color: #0c0c0c;color:green;">
    </pre>


  </d2-container>
</template>

<script>
import {getselecthostgroup,getgroup2host} from '@api/batch'
export default {
name: 'cmd',
mounted () {
  this.GetSelectHostgroupData();
},
  data(){
 return {
   form:{
     hostgroup:'',
     host:[],
     cmd:''
   },
   HostData:[],
   HostGroupData:[],
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
  onSubmit() {
    this.initWebSocket();

  },
  initWebSocket(){
    //连接服务器
    this.websocket = new WebSocket("ws://127.0.0.1:8000/ws/cmd/");
    //指定事件回调
    this.websocket.onmessage = this.websocketOnMessage;
    this.websocket.onopen = this.websocketOnOpen;
    this.websocket.onerror = this.websocketOnError;
    this.websocket.onclose = this.websocketClose;
  },
  sendWebSocketMsg(msg){
    this.websocket.send(JSON.stringify(msg))
  },
  websocketOnMessage(e){
    console.log(e.data)
    let data= JSON.parse(e.data)
    if(data.status===0){
      $('#pre').append(data.message+'\n\n');
    }else {
      this.message.error(data.message+'\n\n')
    }
  },
  websocketOnOpen(e){
    console.log(e)
    var data = {
      "hosts": this.form.host,
      "cmd":this.form.cmd,
    }
    this.sendWebSocketMsg(data)
  },
  websocketOnError(e){
    console.log(e)
  },
  websocketClose(e){
    console.log(e)
  },
  GetSelectHostgroupData(){
    getselecthostgroup().then(res=>{
      this.HostGroupData = res
    }).catch(function (error){
      console.log(error)
    })


  },
  changeHostgroup(value){
    getgroup2host({hostgroup:value}).then(res=>{
        this.HostData=res;

      }).catch(function (error){
        console.log(error)
      })

  },
}
}
</script>

<style scoped>

</style>
