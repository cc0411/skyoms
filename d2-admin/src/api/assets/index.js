import request from '@/plugin/axios'

//获取主机信息
export function  gethost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/',
    method: 'get',
    params
  })
}
//获取主机详细信息
export function  gethostinfo(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/'+params+'/',
    method: 'get',
  })
}
//获取CPU监控图
export function  getcpuinfo(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/cpu/chart_json/'+params+'/',
    method: 'get',
  })
}
//获取内存监控图
export function  getmemoryinfo(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/memory/chart_json/'+params+'/',
    method: 'get',
  })
}

//获取主机绑定用户信息
export function  getuserbindhost(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/userbindhost/',
    method: 'get',
    params
  })
}
//获取远程用户
export function  getremoteuser(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/remoteuser/',
    method: 'get',
    params
  })
}

//获取主机组信息
export function  gethostgroup(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/hostgroup/',
    method: 'get',
    params
  })
}

//添加主机组
export function addhostgroup(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/hostgroup/',
    method: 'post',
    data: params
  })
}
//更新主机组
export function updatehostgroup(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/hostgroup/' + params.id + '/',
    method: 'patch',
    data: params
  })
}
//删除主机组
export function deletehostgroup(id){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/hostgroup/' + id + '/',
    method:'delete'
  })
}

//添加远程用户
export function addremoteuser(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/remoteuser/',
    method: 'post',
    data: params
  })
}

//更新远程用户
export function updateremoteuser(id,params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/remoteuser/' + id + '/',
    method: 'patch',
    data: params
  })
}
//删除远程用户
export function deleteremoteuser(id){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/remoteuser/' + id + '/',
    method:'delete'
  })
}

//添加主机
export function addhost(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/',
    method: 'post',
    data: params
  })
}

//更新主机
export function updatehost(id,params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/' + id + '/',
    method: 'patch',
    data: params
  })
}
//删除主机
export function deletehost(id){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/host/' + id + '/',
    method:'delete'
  })
}

//添加主机绑定
export function adduserbindhost(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/userbindhost/',
    method: 'post',
    data: params
  })
}

//更新主机绑定
export function updateuserbindhost(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/userbindhost/' + params.id + '/',
    method: 'patch',
    data: params
  })
}
// 更新绑定主机的属组
export function updatehost2group(id, data) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/api/assets/host2group/' + id + '/',
    method: 'patch',
    data
  })
}
// 删除主机组的成员
export function deleteHostGroupMember(id, params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/api/assets/hostgroupmember/' + id + '/',
    method: 'delete',
    data: params
  })
}

//删除主机绑定信息
export function deleteuserbindhost(id){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/userbindhost/' + id + '/',
    method:'delete'
  })
}


//Ansible更新主机硬件信息
export  function update_hostinfo(params){
  return request({
    url: process.env.VUE_APP_BASE_API + '/api/assets/update_hostinfo/',
    method: 'post',
    data:params,
  })
}
