import request from '@/plugin/axios'

export function  getloginrecord(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/users/loginrecord/',
    method: 'get',
    params
  })
}
