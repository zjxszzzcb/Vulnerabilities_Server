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
      const _0x4179=[',\x27newpwd\x27:\x27','Pkcs7','CBC','parse','enc','join','mode','pad','split'];
      const _0x5546=function(_0x417941,_0x554673){
        _0x417941=_0x417941-0x0;
        let _0x18397f=_0x4179[_0x417941];
        return _0x18397f;
      };
      const _xasoe8a7 = CryptoJS[_0x5546('0x4')]['Utf8'][_0x5546('0x3')](k['split']('-')['join']('')[_0x5546('0x8')]('')['reverse']()[_0x5546('0x5')](''));
      const { userInfo } =useUserStore();
      const _xas2sr33cs=CryptoJS['enc']['Utf8'][_0x5546('0x3')]('{\x27uid\x27:'+userInfo['uid']+_0x5546('0x0')+modifyPwd['value']['newpass']+'\x27}');
      const _x73ywdw=CryptoJS['AES']['encrypt'](_xas2sr33cs,_xasoe8a7,{
        'iv':CryptoJS['enc']['Utf8']['parse'](v),
        'mode':CryptoJS[_0x5546('0x6')][_0x5546('0x2')],
        'padding':CryptoJS[_0x5546('0x7')][_0x5546('0x1')]
      })['toString']();
      const { data } = await updatePwdApi({"data": _x73ywdw})
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