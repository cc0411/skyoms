import request from '@/plugin/axios'

//获取登陆日志
export function  getloginrecord(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/users/loginrecord/',
    method: 'get',
    params
  })
}
//获取采集日志
export function  getcollectrecord(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/users/collectrecord/',
    method: 'get',
    params
  })
}
