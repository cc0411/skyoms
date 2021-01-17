import request from '@/plugin/axios'


// 获取用户列表
export function getUserList(params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/users/',
    method: 'get',
    params
  })
}

// 创建用户
export function createUser(params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/users/',
    method: 'post',
    data: params
  })
}

// 更新用户
export function updateUser(params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/users/' + params.id + '/',
    method: 'patch',
    data: params
  })
}

// 删除用户
export function deleteUser(id) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/users/' + id + '/',
    method: 'delete'
  })
}

// 更新用户的属组
export function updateUserGroup(id, data) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/usergroup/' + id + '/',
    method: 'patch',
    data
  })
}

// 更新用户的属组
export function changeUserPass(id, data) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/chuserpasswd/' + id + '/',
    method: 'put',
    data
  })
}

// 获取用户组列表
export function getGroupList(params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/groups/',
    method: 'get',
    params
  })
}

// 创建用户组
export function createGroup(params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/groups/',
    method: 'post',
    data: params
  })
}

// 更新用户组
export function updateGroup(params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/groups/' + params.id + '/',
    method: 'patch',
    data: params
  })
}

// 删除用户组
export function deleteGroup(id) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/groups/' + id + '/',
    method: 'delete'
  })
}

// 删除用户组的成员
export function deleteGroupMember(id, params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/groupmember/' + id + '/',
    method: 'delete',
    data: params
  })
}

// 获取权限
export function getPermission() {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/permission/',
    method: 'get'
  })
}

// 更新用户组权限
export function updateGroupPerm(id, params) {
  return request({
    url: process.env.VUE_APP_BASE_API +'/users/groupperm/' + id + '/',
    method: 'patch',
    data: params
  })
}
