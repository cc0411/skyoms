import request from '@/plugin/axios'

export function  getselecthostgroup(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/gethostgroup/',
    method: 'get',
    params
  })
}

export function  getgroup2host(params) {
  return request ({
    url: process.env.VUE_APP_BASE_API + '/api/assets/getgroup2host/',
    method: 'get',
    params
  })
}
