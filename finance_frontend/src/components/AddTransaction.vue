<template>
  <el-card class="add-transaction">
    <template #header>
      <div class="card-header">
        <span>添加交易记录</span>
      </div>
    </template>
    
    <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
      <el-form-item label="交易类型" prop="type">
        <el-radio-group v-model="form.type">
          <el-radio-button label="收入">收入</el-radio-button>
          <el-radio-button label="支出">支出</el-radio-button>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="金额" prop="amount">
        <el-input-number 
          v-model="form.amount" 
          :min="0.01" 
          :step="0.01" 
          :precision="2"
          placeholder="请输入金额"
        />
      </el-form-item>
      
      <el-form-item label="分类" prop="category">
        <el-input v-model="form.category" placeholder="例如：餐饮、购物、工资等" />
      </el-form-item>
      
      <el-form-item label="备注">
        <el-input 
          v-model="form.description" 
          type="textarea" 
          :rows="2" 
          placeholder="可选备注信息"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          添加记录
        </el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { financeAPI } from '../services/api'

const emit = defineEmits(['transaction-added'])

const formRef = ref()
const loading = ref(false)

const form = reactive({
  type: '支出',
  amount: null,
  category: '',
  description: ''
})

const rules = {
  type: [{ required: true, message: '请选择交易类型', trigger: 'change' }],
  amount: [
    { required: true, message: '请输入金额', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '金额必须大于0', trigger: 'blur' }
  ],
  category: [{ required: true, message: '请输入分类', trigger: 'blur' }]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
    
    loading.value = true
    await financeAPI.addTransaction(form)
    
    ElMessage.success('交易记录添加成功')
    emit('transaction-added')
    handleReset()
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '添加失败')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  form.type = '支出'
}
</script>

<style scoped>
.add-transaction {
  margin-bottom: 20px;
}
</style>