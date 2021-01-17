import request from '@/plugin/axios'

export function AccountLogin (data) {
  // console.log(process.env)
  return request({
    url: process.env.VUE_APP_BASE_API + '/users/login/',
    method: 'post',
    data,
  })
}
export function getInfo(token) {
  return request({
    url: process.env.VUE_APP_BASE_API + '/users/personinfo/',
    method: 'get',
    params: { token }
  })
}
