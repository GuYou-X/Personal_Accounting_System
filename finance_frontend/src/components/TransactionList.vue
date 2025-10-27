<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>交易记录</span>
        <el-button type="primary" :icon="Refresh" @click="refreshList">
          刷新
        </el-button>
      </div>
    </template>
    
    <el-table :data="transactions" v-loading="loading" style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="date" label="日期" width="180" />
      <el-table-column prop="type" label="类型" width="80">
        <template #default="scope">
          <el-tag :type="scope.row.type === '收入' ? 'success' : 'danger'">
            {{ scope.row.type }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="amount" label="金额" width="120">
        <template #default="scope">
          <span :class="scope.row.type === '收入' ? 'income' : 'expense'">
            {{ scope.row.type === '收入' ? '+' : '-' }}{{ scope.row.amount }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="category" label="分类" width="120" />
      <el-table-column prop="description" label="备注" />
      <el-table-column label="操作" width="100">
        <template #default="scope">
          <el-button 
            size="small" 
            type="danger" 
            @click="handleDelete(scope.row.id)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination" v-if="transactions.length > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
      />
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { financeAPI } from '../services/api'

const transactions = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)

const total = computed(() => transactions.value.length)

const pagedTransactions = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return transactions.value.slice(start, end)
})

const loadTransactions = async () => {
  try {
    loading.value = true
    const response = await financeAPI.getTransactions()
    transactions.value = response.data
  } catch (error) {
    ElMessage.error('加载交易记录失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
      type: 'warning'
    })
    
    await financeAPI.deleteTransaction(id)
    ElMessage.success('删除成功')
    loadTransactions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const refreshList = () => {
  loadTransactions()
}

defineExpose({
  refreshList
})

onMounted(() => {
  loadTransactions()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.income {
  color: #67c23a;
  font-weight: bold;
}

.expense {
  color: #f56c6c;
  font-weight: bold;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>