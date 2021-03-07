import request from '@/plugin/axios'

//获取集群信息
export function  getcluster(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/cluster/',
    method: 'get',
    params
  })
}
//获取数据中心信息
export function  getdatacenter(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/datacenter/',
    method: 'get',
    params
  })
}
//获取存储信息
export function  getdatastore(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/datastore/',
    method: 'get',
    params
  })
}
//获取网络信息
export function  getnetworkadapter(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/networkadapter/',
    method: 'get',
    params
  })
}
//获取宿主机信息
export function  getdedicatedhost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/dedicatedhost/',
    method: 'get',
    params
  })
}
//获取虚拟机信息
export function  getvirtualhost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/virtualhost/',
    method: 'get',
    params
  })
}
//获取集群中的所有主机数量
export function  getclusterhost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/getclusterhost/',
    method: 'get',
    params
  })
}
//获取宿主机资源信息
export function  gethostresource(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/gethostresource/',
    method: 'get',
    params
  })
}
//获取系统版本
export function  getsystemresource(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/getsystemdata/',
    method: 'get',
    params
  })
}
//获取存储资源信息
export function  getdataresource(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/getdataresource/',
    method: 'get',
    params
  })
}
//获取数据中心用于过滤
export function  gettreedata(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/gettreedata/',
    method: 'get',
    params
  })
}
