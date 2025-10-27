<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>财务统计</span>
        <el-button :icon="Refresh" @click="loadStatistics">刷新</el-button>
      </div>
    </template>
    
    <div v-loading="loading">
      <!-- 财务概览 -->
      <el-row :gutter="20" class="overview">
        <el-col :span="8">
          <el-statistic title="总收入" :value="stats.total_income" precision="2">
            <template #prefix>
              <el-icon><Money /></el-icon>
            </template>
            <template #suffix>元</template>
          </el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic title="总支出" :value="stats.total_expense" precision="2">
            <template #prefix>
              <el-icon><Money /></el-icon>
            </template>
            <template #suffix>元</template>
          </el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic 
            title="当前余额" 
            :value="stats.balance" 
            :value-style="balanceStyle"
            precision="2"
          >
            <template #prefix>
              <el-icon><Wallet /></el-icon>
            </template>
            <template #suffix>元</template>
          </el-statistic>
        </el-col>
      </el-row>
      
      <!-- 支出分类统计 -->
      <el-divider content-position="left">支出分类统计</el-divider>
      <el-table :data="categoryData" v-if="categoryData.length > 0">
        <el-table-column prop="category" label="分类" />
        <el-table-column prop="amount" label="金额">
          <template #default="scope">
            {{ scope.row.amount.toFixed(2) }} 元
          </template>
        </el-table-column>
        <el-table-column prop="percentage" label="占比">
          <template #default="scope">
            <el-progress 
              :percentage="scope.row.percentage" 
              :show-text="false"
            />
            {{ scope.row.percentage.toFixed(1) }}%
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无支出数据" />
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Money, Wallet } from '@element-plus/icons-vue'
import { financeAPI } from '../services/api'

const stats = ref({
  total_income: 0,
  total_expense: 0,
  balance: 0,
  expense_by_category: {}
})

const loading = ref(false)

const balanceStyle = computed(() => ({
  color: stats.value.balance >= 0 ? '#67c23a' : '#f56c6c'
}))

const categoryData = computed(() => {
  const categories = stats.value.expense_by_category
  const total = stats.value.total_expense
  
  return Object.entries(categories).map(([category, amount]) => ({
    category,
    amount,
    percentage: total > 0 ? (amount / total) * 100 : 0
  })).sort((a, b) => b.amount - a.amount)
})

const loadStatistics = async () => {
  try {
    loading.value = true
    const response = await financeAPI.getStatistics()
    stats.value = response.data
  } catch (error) {
    ElMessage.error('加载统计信息失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
.overview {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>