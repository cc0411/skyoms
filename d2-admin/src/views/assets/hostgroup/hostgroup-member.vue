<template>
  <div class="groupmember">
    <el-table
      :data="values"
      style="width: 100%">
      <el-table-column
        label="IP"
        min-width= "150"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ip }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="60">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="danger"
            @click="MemberDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
name: "hostgroup-member",
props: {
    values: {
      type: Array,
      default: () => []
    }
  },
methods: {
    MemberDelete(value) {
      this.$confirm(`此操作将${value.ip}用户移出该成员组, 是否继续?`, '移除主机', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', value)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消移除'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>
