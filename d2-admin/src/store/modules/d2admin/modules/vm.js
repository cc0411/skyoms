import {gettreedata} from '@api/vms'

const state = () => ({
  cluster:[],
  datacenter:[],
  datastore:[],
  virtualhost:[],
  treeData:[],
});
const getters = {
 treeData: state=>state.treeData

};
const mutations = {
  setTreeData(state,params){
    state.treeData = params;
  }
}
const actions = {
  async fetTreeData({commit}){
    try {
      const res = await gettreedata();
      commit('setTreeData',res)
    }
  catch (err){
      console.log(err)
    }}
}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
