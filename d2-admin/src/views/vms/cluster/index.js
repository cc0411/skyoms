let _this =null;
const sendThis = e=>{
  _this =e;
}

const tableColumns = [
  {
    label: '集群名',
    prop: 'name',
    sort:false,
    width: 120,
    istrue: true
  },
  {
    label: '数据中心',
    prop: 'datacenter',
    sort:false,
    width:150,
    istrue: true
  },
  {
    label: 'CPU总计/G',
    prop: 'cputotal',
    sort:false,
    width: 130,
    istrue: true
  },
  {
    label: 'CPU使用量/Ghz',
    prop: 'cpuusage',
    sort:false,
    width: 130,
    istrue: true
  },
  {
    label: '内存总计/G',
    prop: 'memtotal',
    sort:false,
    width: 130,
    istrue: true
  },
  {
    label: '内存使用量/G',
    prop: 'memusage',
    sort:false,
    width: 130,
    istrue: true
  },
  {
    label: '存储总计/T',
    prop: 'datatotal',
    sort:false,
    width: 130,
    istrue: true
  },
  {
    label: '存储剩余量/T',
    prop: 'datafree',
    sort:"custom",
    width: 130,
    istrue: true
  },
  {
    label: '宿主机数量',
    prop: 'numshosts',
    sort:"custom",
    width:120,
    istrue: true
  },
  {
    label: '虚拟机数量',
    prop: 'vmscount',
    sort:"custom",
    width: 120,
    istrue: true
  },
  {
    label: '状态',
    prop: 'overallstatus',
    sort: false,
    width: 110,
    istrue: true,
    render: row=>{
      if(row.overallstatus==='green'){
        return "<span style='background-color: #5daf34'>正常</span>";
      }else if(row.overallstatus==='red'){
        return '异常';
      }
    }
  }
]

export {
  tableColumns,
  sendThis
}
