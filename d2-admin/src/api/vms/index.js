import request from '@/plugin/axios'
export function  getcluster(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/cluster/',
    method: 'get',
    params
  })
}
export function  getdatacenter(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/datacenter/',
    method: 'get',
    params
  })
}
export function  getdatastore(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/datastore/',
    method: 'get',
    params
  })
}
export function  getnetworkadapter(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/networkadapter/',
    method: 'get',
    params
  })
}
export function  getdedicatedhost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/dedicatedhost/',
    method: 'get',
    params
  })
}
export function  getvirtualhost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/virtualhost/',
    method: 'get',
    params
  })
}
export function  getclusterhost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/getclusterhost/',
    method: 'get',
    params
  })
}
export function  gethostresource(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/gethostresource/',
    method: 'get',
    params
  })
}

export function  getsystemresource(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/getsystemdata/',
    method: 'get',
    params
  })
}
export function  getdataresource(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/getdataresource/',
    method: 'get',
    params
  })
}
export function  gettreedata(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/vms/gettreedata/',
    method: 'get',
    params
  })
}
