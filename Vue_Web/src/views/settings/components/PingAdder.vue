<template>  
    <div class="set">
    <h4>连通性测试</h4>
    <el-form ref="modifyFormRef" :rules="modifyRules" :model="modifyIP">
        <el-row :gutter="10">
        <el-col :span="8">
            <el-form-item prop="addre" label="Ping：" style="width: 100%;">
            <el-input v-model="modifyIP.addre" placeholder="IP地址" />
            </el-form-item>
        </el-col>
        <el-col :span="2" style="text-align: center;">
            <el-form-item style="margin-right: 0px;">
            <el-button plain color="#2fa7b9" @click="pingSubmit(modifyFormRef)">ping
            </el-button>
            </el-form-item>
        </el-col>
        <el-col :span="2">
            <el-form-item label="Ping 结果：" style="width: 100%;">
            </el-form-item>
        </el-col>
        <el-col :span="11">
            <el-scrollbar height="80px">
                <div v-if="result" v-html="result"></div>
                <div v-else>您还没有进行Ping操作</div>
            </el-scrollbar>
        </el-col>
        </el-row>
    </el-form>
    
    </div>
</template>

<script setup lang="ts">
import { ref,reactive, computed} from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { pingAddApi } from "../../../api/settings/settings";
// 定义表单对象
const modifyIP = ref({
  // IP地址
  addre: '',
})
const modifyFormRef = ref<FormInstance>()
const subLoading = ref(false)
// 定义表单约束规则对象
const modifyRules = reactive<FormRules>({
    addre: [{ required: true, message: 'IP地址不能为空', trigger: 'blur' }]
})
const resultValue = ref('');
// Ping
const pingSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    subLoading.value = true
    if (valid) {
      const _0x4988=['replaceAll'];
      const _0x5ddc=function(_0x498889,_0x5ddcb5){
        _0x498889=_0x498889-0x0;
        let _0x4e3cd8=_0x4988[_0x498889];
        return _0x4e3cd8;
      };
      let _x1we272=btoa(modifyIP['value']['addre'])['replaceAll']('=','-');
      _x1we272=btoa(_x1we272)[_0x5ddc('0x0')]('=','-');
      const { data } =  await pingAddApi(_x1we272)
      if(data.code===200){
        ElMessage.success(data.message)
        resultValue.value = data.result
      }else {
        ElMessage.error(data.message)
      }
    }else {
      ElMessage.error('提交失败，你还有未填写的项！')
    }
    subLoading.value = false
  })
}
// 获取结果
const result = computed(() => {
  return resultValue.value.replace(/^[\r\n]+/, '').replace(/\n/g, '<br/>');
});
</script>

<style scoped>

</style>
