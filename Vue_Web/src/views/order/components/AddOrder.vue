<template>
  <el-form ref="ruleFormRef" :model="formOrder" label-width="80px">
    <el-row>
      <el-col :span="12">
        <el-form-item label="菜品名">
          <el-select v-model="formOrder.food" placeholder="请选择菜品" style="width: 100%;">
            <el-option v-for="item in orderOptions" :key="item.id" :label="item.foodname" :value="item.foodname" />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="数量">
          <el-input-number v-model="formOrder.num" :min="1"/>
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item label="备注">
          <el-input
              v-model="formOrder.remarks"
              :rows="2"
              type="textarea"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>

  <div class="dialong__button--wrap">
    <el-button @click="close">取消</el-button>
    <el-button color="#178557" :loading="subLoading" type="success" @click="addOrder(ruleFormRef)">保存</el-button>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue'
import {ElMessage} from 'element-plus'
import {addOrderApi,getAllFoodListApi} from "../../../api/order/order";
import type { FormInstance, FormRules } from 'element-plus'
const ruleFormRef = ref<FormInstance>()

const subLoading = ref(false)
const emit = defineEmits(['closeAddOrderForm','success'])
const formOrder = reactive({
  food: '',
  num: 0,
  remarks: '',
})
// 新增订单信息
const addOrder = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    subLoading.value = true
    if (valid) {
      const { data } =  await addOrderApi(formOrder)
      if(data.code===200){
        ElMessage.success(data.message)
        emit('success')
      }else {
        ElMessage.error(data.message)
      }
    } else {
      ElMessage.error('提交失败，你还有未填写的项！')
      console.log('error submit!', fields)
    }
    subLoading.value = false
  })
}
// 取消表单
const close = ()=> {
  emit('closeAddOrderForm')
}
// 定义角色下拉选择项
const orderOptions = ref<object[]>([])
// 获取所有角色列表
async function getAllOrderList() {
  try {
    const { data } = await getAllFoodListApi()
    if (data.code === 200) {
      orderOptions.value = data.result.list
    }
  } catch (e) {
    console.log(e)
  }
}
getAllOrderList()
</script>

<style scoped>
.dialong__button--wrap {
  text-align: center;
  margin-top: 20px;
}
</style>
