import {getInfo} from '@api/sys.login'

const state = () => ({
  token:'',
  username:'',
  is_superuser:''

})
const getters = {
  token: state=>state.token,
  username: state=>state.username,
  is_superuser: state=>state.is_superuser,
};


const mutations = {
  SET_TOKEN(state,params){
    state.token = params;
  },
  SET_USERNAME(state,params){
    state.username = params
  },
  SET_IS_SUPERUSER(state,params){
    state.is_superuser = params
  }
};
const actions = {
  // 获取用户信息
  GetInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        commit('SET_USERNAME', response.username)
        commit('SET_IS_SUPERUSER', response.is_superuser)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },


}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
