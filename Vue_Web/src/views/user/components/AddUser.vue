<template>

  <el-form ref="ruleFormRef" :rules="rules"  :model="formUser"  label-width="80px">
    <el-row>
      <el-col :span="24">
        <el-form-item prop="role" label="所属角色">
          <el-select v-model="formUser.role_id" placeholder="请选择角色" style="width: 100%;">
            <el-option v-for="item in roleOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
      </el-col>
    <el-col :span="12">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="formUser.username" placeholder="请输入用户名" />
    </el-form-item>
    </el-col>
    <el-col :span="12">
    <el-form-item label="登录密码" prop="password">
      <el-input v-model="formUser.password" placeholder="请输入密码" />
    </el-form-item>
    </el-col>
      <el-col :span="12">
    <el-form-item label="电话" prop="phone">
      <el-input v-model="formUser.phone" placeholder="请输入电话" />
    </el-form-item>
      </el-col>
      <el-col :span="12">
    <el-form-item label="联系邮箱" prop="email">
      <el-input v-model="formUser.email" placeholder="请输入联系邮箱" />
    </el-form-item>
      </el-col>
      <el-col :span="12">
    <el-form-item label="性别" prop="sex">
      <el-radio-group v-model="formUser.sex" fill="#178557">
        <el-radio-button label="男" />
        <el-radio-button label="女" />
      </el-radio-group>
    </el-form-item>
      </el-col>
      <el-col :span="12">
    <el-form-item label="状态" prop="status">
      <el-radio-group v-model="formUser.status" fill="#178557">
        <el-radio :label=true>正常</el-radio>
        <el-radio :label=false>封禁</el-radio>

      </el-radio-group>
    </el-form-item>
      </el-col>

      <el-col :span="24">
        <el-form-item label="备注">
          <el-input
              v-model="formUser.remarks"
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
    <el-button color="#178557" :loading="subLoading" type="success" @click="addUser(ruleFormRef)">保存</el-button>
  </div>
</template>

<script setup lang="ts">
import { reactive,ref } from 'vue'
import { ElMessage } from 'element-plus'
import {addUserApi, getAllRoleListApi} from "../../../api/user/user"
import type { FormInstance, FormRules } from 'element-plus'
const emit = defineEmits(['closeAddUserForm','success'])
const subLoading = ref(false)
const ruleFormRef = ref<FormInstance>()
const formUser = reactive({
  username: '',
  password: '',
  status: false,
  phone: '',
  email: '',
  sex: '男',
  remarks: '',
  role_id: null,
})
// 定义表单约束规则对象
const rules = reactive<FormRules>({
  username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
  password: [{ required: true, message: '登录密码不能为空', trigger: 'blur' }],
  role_id: [{ required: true, message: '角色不能为空', trigger: 'blur' }],
})

// 新增用户信息
const addUser = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    subLoading.value = true
    if (valid) {
      const { data } =  await addUserApi(formUser)
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

// 定义角色下拉选择项
const roleOptions = ref<object[]>([])
// 获取所有角色列表
async function getAllRoleList() {
  try {
    const { data } = await getAllRoleListApi()
    if (data.code === 200) {
      roleOptions.value = data.result.list
    }
  } catch (e) {
    console.log(e)
  }
}
getAllRoleList()
// 取消表单
const close = ()=> {
  emit('closeAddUserForm')
}
</script>

<style scoped>
.dialong__button--wrap {
  text-align: center;
  margin-top: 20px;
}
</style>
