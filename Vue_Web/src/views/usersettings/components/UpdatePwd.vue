<template>
  <div class="set">
    <h4>修改密码</h4>
    <p style="display: inline-flex;
                    justify-content: center;
                    align-items: center;">
      <el-icon style="margin-right: 5px;">
        <CircleCheck />
      </el-icon>密码6~18位字母、数字、特殊字符组成
    </p>
    <el-form ref="modifyFormRef" :rules="modifyRules" :model="modifyPwd" class="demo-form-inline">
      <el-row :gutter="20">
        <el-col :span="10">
          <el-form-item prop="newpass" label="新密码：" style="width: 100%;">
            <el-input v-model="modifyPwd.newpass" show-password placeholder="请输入新密码" />
          </el-form-item>
        </el-col>
        <el-col  :span="4" style="text-align: center;">
          <el-form-item style="margin-right: 0px;">
            <el-button plain color="#2fa7b9" :loading="subLoading" @click="modifySubmit(modifyFormRef)">提交
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive} from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { updatePwdApi } from "../../../api/usersettings/usersettings";
import { useUserStore } from '../../../store/modules/user'
import CryptoJS from 'crypto-js'

// 定义表单对象
const modifyPwd = ref({
  // 新密码
  newpass: ''
})
const k = "2e2-48fc60d-4433b-898-e42cbc9-1d7eff8";
const modifyFormRef = ref<FormInstance>()
const subLoading = ref(false)
const v = "1cfc13bd74a2";
// 定义表单约束规则对象
const modifyRules = reactive<FormRules>({
  newpass: [{ required: true, message: '新密码不能为空', trigger: 'blur' }]
})

// 提交修改密码
const modifySubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    subLoading.value = true
    if (valid) {
      const key = CryptoJS.enc.Utf8.parse(k.split('-').join('').split('').reverse().join(''));
      const { userInfo } =  useUserStore()
      const srcs = CryptoJS.enc.Utf8.parse("{'uid':"+userInfo.uid+",'newpwd':'"+modifyPwd.value.newpass+"'}");
      const { data } = await updatePwdApi({"data":CryptoJS.AES.encrypt(srcs, key, {
        iv: CryptoJS.enc.Utf8.parse(v),
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
      }).toString()})
      if(data.code===200){
        ElMessage.success(data.message)
      }else {
        ElMessage.error(data.message)
      }
    }else {
      ElMessage.error('提交失败，你还有未填写的项！')
    }
    subLoading.value = false
  })
}
</script>

<style scoped>

</style>
