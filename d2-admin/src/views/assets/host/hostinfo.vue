<template>
  <d2-container type="card">
    <b-row>
      <b-col cols="4">
        <b-card
        border-variant="info"
        header="硬件信息"
        header-bg-variant="info"
        header-text-variant="white"
        align="left"
      >
        <b-list-group flush>
          <b-list-group-item>IP: {{InfoData.server}}</b-list-group-item>
          <b-list-group-item>物理CPU数: {{InfoData.cpu_number}}</b-list-group-item>
          <b-list-group-item>逻辑CPU数: {{InfoData.vcpu_number}}</b-list-group-item>
          <b-list-group-item>内存: {{InfoData.memory}}G</b-list-group-item>
          <b-list-group-item>硬盘: {{InfoData.disk}}G</b-list-group-item>
        </b-list-group>
      </b-card>
      </b-col>
      <b-col cols="8">
        <b-card
        border-variant="primary"
        header="CPU"
        header-bg-variant="primary"
        header-text-variant="white"
        align="center"
      >
        <b-card-text>
          <highcharts :options="CpuOptions" :callback="getCpuInfoData"></highcharts>
        </b-card-text>
      </b-card>
      </b-col>
    </b-row>

    <b-row  style="margin-top: 10px">
      <b-col cols="4">
        <b-card
        border-variant="warning"
        header="系统信息"
        header-bg-variant="warning"
        header-text-variant="white"
        align="left"
      >
        <b-list-group flush>
          <b-list-group-item>CPU: {{InfoData.cpu_info}}</b-list-group-item>
          <b-list-group-item>系统: {{InfoData.os}}</b-list-group-item>
          <b-list-group-item>内核: {{InfoData.os_kernel}}</b-list-group-item>
          <b-list-group-item>类型: {{InfoData.server_model}}</b-list-group-item>
          <b-list-group-item>文件系统: {{InfoData.filesystems}}</b-list-group-item>
        </b-list-group>
      </b-card>
      </b-col>
      <b-col cols="8">
        <b-card
        border-variant="success"
        header="内存"
        header-bg-variant="success"
        header-text-variant="white"
        align="center"
      >
        <b-card-text >
          <highcharts :options="MemoryOptions" :callback="getMemoryData"></highcharts>
        </b-card-text>
      </b-card>
      </b-col>
    </b-row>
  </d2-container>
</template>

<script>
import Highcharts from 'highcharts'
import exportingInit from 'highcharts/modules/exporting'
exportingInit(Highcharts)
import {gethostinfo,getcpuinfo,getmemoryinfo} from '@/api/assets'
export default {
name: 'hostinfo',
mounted () {
    this.getHostInfoData();
  },
computed:{
  id:function (){
    return this.$route.params.id
  }
},
data(){
    return {
    InfoData:[],
    CpuOptions:{
      chart: {
        zoomType: 'x',
        //height: 240,
        //type: 'line'
      },
      credits:{
        enabled:false
      },
      global: {
        useUTC: false
      },
      title: {
        text: 'cpu使用率'
      },
      lang: {
        printChart: '打印图表',
        downloadPNG: '下载JPEG 图片',
        downloadJPEG: '下载JPEG文档',
        downloadPDF: '下载PDF 文件',
        downloadSVG: '下载SVG 矢量图'
      },
      subtitle: {
        text: document.ontouchstart === undefined ?
          '单击并拖动绘图区域以放大' : '捏合图表放大'
      },
      xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: {
          millisecond: '%H:%M:%S.%L',
          second: '%H:%M:%S',
          minute: '%H:%M',
          hour: '%H:%M',
          day: '%m-%d',
          week: '%m-%d',
          month: '%Y-%m',
          year: '%Y'
        }
      },
      tooltip: {
        formatter: function () {
          return '<strong>' + this.series.name + ':' + this.y + '%<br/></strong>' +
            Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x);
        }
      },
      yAxis: {
        title: {
          text: '使用率'
        }
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        area: {
          fillColor: {
            linearGradient: {
              x1: 0,
              y1: 0,
              x2: 0,
              y2: 1
            },
            stops: [
              [0, new Highcharts.getOptions().colors[0]],
              [1, new Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            ]
          },
          marker: {
            radius: 2
          },
          lineWidth: 1,
          states: {
            hover: {
              lineWidth: 1
            }
          },
          threshold: null
        }
      },

      series: [{
        type: 'area',
        name: 'Usage',
        data: []
      }]

    },
    MemoryOptions:{
      chart: {
        zoomType: 'x',

      },
      credits:{
        enabled:false
      },
      global: {
        useUTC: false
      },
      title: {
        text: '内存使用率'
      },
      lang: {
        printChart: '打印图表',
        downloadPNG: '下载JPEG 图片',
        downloadJPEG: '下载JPEG文档',
        downloadPDF: '下载PDF 文件',
        downloadSVG: '下载SVG 矢量图'
      },
      subtitle: {
        text: document.ontouchstart === undefined ?
          '单击并拖动绘图区域以放大' : '捏合图表放大'
      },
      xAxis: {
        type: 'datetime',
      },
      tooltip: {
        formatter: function () {
          return '<strong>' + this.series.name + ':' + this.y + '%<br/></strong>' +
            Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x);
        }
      },
      yAxis: {
        title: {
          text: '使用率'
        }
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        area: {
          fillColor: {
            linearGradient: {
              x1: 0,
              y1: 0,
              x2: 0,
              y2: 1
            },
            stops: [
              [0, Highcharts.getOptions().colors[0]],
              [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            ]
          },
          marker: {
            radius: 2
          },
          lineWidth: 1,
          states: {
            hover: {
              lineWidth: 1
            }
          },
          threshold: null
        }
      },
      series: [{
        type: 'area',
        name: 'Usage',
        data: []
      }]
    },

    }
},
methods :{
  getCpuInfoData(){
    getcpuinfo(this.id).then(res=>{
      this.CpuOptions.series[0].data = res
    }).catch(function (error){
      console.log(error)
    })
  },
  getMemoryData(){
    getmemoryinfo(this.id).then(res=>{
      this.MemoryOptions.series[0].data = res
    }).catch(function (error){
      console.log(error)
    })
  },
  getHostInfoData(){
    gethostinfo(this.id).then(res=>{
      this.InfoData = res;
      console.log(this.InfoData)
    }).catch(function (error){
      console.log(error)
    })
  },
}
}
</script>

<style scoped>

</style>
