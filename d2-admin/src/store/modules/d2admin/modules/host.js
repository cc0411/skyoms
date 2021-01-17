import {getcpuinfo,getmemoryinfo} from '@/api/assets'

const state = () => ({
  CpuInfo:[],
  MemoryInfo:[],
});
const getters = {
  CpuInfo: state=>state.CpuInfo,
  MemoryInfo: state=>state.MemoryInfo
};
const mutations = {
  setCpuInfoData(state,params){
    state.CpuInfo= params;
  },
  setMemoryInfoData(state,params){
    state.MemoryInfo= params;
  }
};
const actions = {
  async fetCpuInfoData({commit,id}){
    try {
      const res = await getcpuinfo(id);
      commit('setCpuInfoData',res)
    }
    catch (err){
      console.log(err)
    }},
  async fetMemoryInfoData({commit,id}){
    try {
      const res = await getmemoryinfo(id);
      commit('setMemoryInfoData',res)
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

