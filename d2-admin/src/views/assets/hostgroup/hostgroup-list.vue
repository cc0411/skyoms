<template>
<div class="grouplist">
  <el-table
    v-loading="loading"
    :data="values"
    v-if="values.length>0"
    style="width: 100%">
    <el-table-column
      prop="name"
      label="组名"
      width="110"
    ></el-table-column>
    <el-table-column
      label="成员"
    >
      <template slot-scope="scope">
        <el-button type="text" @click="groupMember(scope.row)">{{ scope.row.hosts.length }}</el-button>
      </template>
    </el-table-column>
    <el-table-column
      prop="desc"
      label="描述"
      width="300">
    </el-table-column>
    <el-table-column
      label="操作"
      width="200"
      align="center"
    >
      <template slot-scope="scope">
        <el-button  size="mini" @click="handleEdit(scope.row)" >编辑</el-button>
        <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
      </template>

    </el-table-column>
  </el-table>
</div>
</template>

<script>
export default {
name: "hostgroup-list",
props: {
    values: {
      type: Array,
      default: function() {
        return []
      }
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    handleEdit(group) {
      this.$emit('edit', group)
    },
    handleDelete(group) {
      this.$confirm(`此操作将删除该${group.name}组记录, 是否继续?`, '删除组', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', group.id)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    groupMember(group) {
      this.$emit('list', group)
    }

  }

}
</script>

<style scoped>

</style>
