<template>
  <d2-container>
    <template slot="header">仪表盘</template>
    <b-row style="margin-top: 10px">
      <b-col cols="6">
        <b-card
          border-variant="info"
          header="系统类型数据展示"
          header-bg-variant="info"
          header-text-variant="white"
          align="center"
        >
          <b-card-text>
            <ve-pie :data="SystemData" :settings="chartSettings"></ve-pie>
          </b-card-text>
          <div style="float: left">
            <el-select v-model="getParams.datacenter" class="d2-mr-5" size="mini"  placeholder="请选择数据中心"  @change="GetSystemData">
              <el-option
                v-for="item in treeData"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </div>
        </b-card>
      </b-col>
    </b-row>
    <b-row style="margin-top: 10px">
      <b-col>
        <b-card
          border-variant="info"
          header="集群资源展示"
          header-bg-variant="info"
          header-text-variant="white"
          align="center"
        >
          <b-card-text>
            <ve-histogram :data="ClusterData"></ve-histogram>
          </b-card-text>
        </b-card>
      </b-col>
    </b-row>
    <b-row style="margin-top: 10px">
      <b-col>
        <b-card
          border-variant="info"
          header="宿主机资源展示"
          header-bg-variant="info"
          header-text-variant="white"
          align="center"
        >
          <b-card-body>

            <b-card-text>
              <ve-line :data="HostData" :extend="extend"></ve-line>
            </b-card-text>
            <div style="float: right">
              <el-select v-model="getParams.datacenter" class="d2-mr-5" size="mini"  placeholder="请选择数据中心"  @change="GetdedicatehostresourceData">
                <el-option
                  v-for="item in treeData"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </div>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
    <template slot="footer">footer</template>
  </d2-container>
</template>

<script>
import {getclusterhost,gethostresource,getsystemresource} from '@api/vms'
import {createNamespacedHelpers} from 'vuex'
const {mapState} = createNamespacedHelpers('d2admin')
export default {
  name: "dashboard",
  mounted () {
    this.GetClusterhostData()
    this.GetdedicatehostresourceData()
    this.GetSystemData()
    this.$store.dispatch('d2admin/vm/fetTreeData')
  },
  computed:{
    ...mapState({
      treeData: state=>state.vm.treeData
    })
  },
  data () {
    this.extend={
     'xAxis.0.axisLabel.rotate':45
    }
    this.chartSettings = {
      offsetY:320,
      radius: 80
    }
    return {
      ClusterData: {
        columns: ['集群', '虚拟机数量', '宿主机数量' ],
        rows: []
      },
      SystemData:{
        rows:[],
        columns:['系统类型','数量']
      },
      HostData:{
        columns:['主机名','cpu总计/GHz','cpu已用/GHz','内存总计/G','内存已用/G'],
        rows:[]
      },
      getParams:{datacenter: ''}

    }
  },
  methods:{
    GetClusterhostData(){
      getclusterhost().then(res=>{
        this.ClusterData.rows = res;
        console.log(this.ClusterData.rows)
      }).catch(function (error){
        console.log(error)
      })
    },
    GetSystemData(){
      getsystemresource(this.getParams).then(res=>{
        this.SystemData.rows=res;
        console.log(this.SystemData.rows)

      }).catch(function (error){
        console.log(error)
      })
    },
    GetdedicatehostresourceData(){
      gethostresource(this.getParams).then(res=>{
        this.HostData.rows = res;
        console.log(this.HostData.rows)
      }).catch(function (error){
        console.log(error)
      })
    },
  }
}

</script>

<style scoped>
</style>
