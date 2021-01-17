import request from '@/plugin/axios'

export function  gethost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/',
    method: 'get',
    params
  })
}
export function  gethostinfo(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/'+params+'/',
    method: 'get',
  })
}
export function  getcpuinfo(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/cpu/chart_json/'+params+'/',
    method: 'get',
  })
}

export function  getmemoryinfo(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/memory/chart_json/'+params+'/',
    method: 'get',
  })
}

export function  getuserbindhost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/userbindhost/',
    method: 'get',
    params
  })
}
export function  getremoteuser(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/remoteuser/',
    method: 'get',
    params
  })
}
export function  gethostgroup(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/hostgroup/',
    method: 'get',
    params
  })
}

export function addhostgroup(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/hostgroup/',
    method: 'post',
    data: params
  })
}

export function updatehostgroup(id,params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/hostgroup/' + id + '/',
    method: 'patch',
    data: params
  })
}
export function deletehostgroup(id){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/hostgroup/' + id + '/',
    method:'delete'
  })
}

export function addremoteuser(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/remoteuser/',
    method: 'post',
    data: params
  })
}

export function updateremoteuser(id,params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/remoteuser/' + id + '/',
    method: 'patch',
    data: params
  })
}
export function deleteremoteuser(id){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/remoteuser/' + id + '/',
    method:'delete'
  })
}

export function addhost(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/',
    method: 'post',
    data: params
  })
}

export function updatehost(id,params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/' + id + '/',
    method: 'patch',
    data: params
  })
}
export function deletehost(id){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/' + id + '/',
    method:'delete'
  })
}

export function adduserbindhost(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/userbindhost/',
    method: 'post',
    data: params
  })
}

export function updateuserbindhost(id,params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/userbindhost/' + id + '/',
    method: 'patch',
    data: params
  })
}
export function deleteuserbindhost(id){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/userbindhost/' + id + '/',
    method:'delete'
  })
}

export  function update_hostinfo(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/update_hostinfo/',
    method: 'post',
    data:params,
  })
}
