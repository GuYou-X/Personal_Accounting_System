<template>
  <div id="app">
    <el-container class="layout">
      <el-header class="header">
        <h1>个人记账系统</h1>
      </el-header>
      
      <el-main class="main">
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane label="添加记录" name="add">
            <AddTransaction @transaction-added="handleTransactionAdded" />
          </el-tab-pane>
          
          <el-tab-pane label="交易记录" name="transactions">
            <TransactionList ref="transactionListRef" />
          </el-tab-pane>
          
          <el-tab-pane label="财务统计" name="statistics">
            <Statistics />
          </el-tab-pane>
          
          <el-tab-pane label="搜索记录" name="search">
            <Search />
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AddTransaction from './components/AddTransaction.vue'
import TransactionList from './components/TransactionList.vue'
import Statistics from './components/Statistics.vue'
import Search from './components/Search.vue'

const activeTab = ref('add')
const transactionListRef = ref()

const handleTransactionAdded = () => {
  // 切换到交易记录标签页并刷新列表
  activeTab.value = 'transactions'
  if (transactionListRef.value) {
    setTimeout(() => {
      transactionListRef.value.refreshList()
    }, 100)
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.layout {
  min-height: 100vh;
}

.header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header h1 {
  margin: 0;
}

.main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>