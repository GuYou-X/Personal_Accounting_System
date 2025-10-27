<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>搜索交易记录</span>
      </div>
    </template>
    
    <el-form :model="searchForm" inline>
      <el-form-item>
        <el-input
          v-model="searchForm.keyword"
          placeholder="输入分类或备注关键词"
          style="width: 300px"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button :icon="Search" @click="handleSearch" />
          </template>
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>
    
    <el-table :data="searchResults" v-loading="loading" v-if="searched">
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
    </el-table>
    
    <div v-if="searched && searchResults.length === 0" class="no-data">
      <el-empty description="未找到相关记录" />
    </div>
  </el-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { financeAPI } from '../services/api'

const searchForm = reactive({
  keyword: ''
})

const searchResults = ref([])
const loading = ref(false)
const searched = ref(false)

const handleSearch = async () => {
  if (!searchForm.keyword.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  
  try {
    loading.value = true
    const response = await financeAPI.searchTransactions(searchForm.keyword)
    searchResults.value = response.data
    searched.value = true
  } catch (error) {
    ElMessage.error('搜索失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  searchForm.keyword = ''
  searchResults.value = []
  searched.value = false
}
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

.no-data {
  margin-top: 20px;
}
</style>