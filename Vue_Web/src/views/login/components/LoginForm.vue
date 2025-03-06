<template>
<el-form
    ref="ruleFormRef"
    :model="ruleForm"
    :rules="rules"
>
  <el-form-item label="" prop="username">
    <el-input placeholder="请输入用户名" autoComplete="on" style="position: relative" v-model="ruleForm.username">
      <template #prefix>
        <el-icon class="el-input__icon"><UserFilled /></el-icon>
      </template>
    </el-input>
  </el-form-item>

  <el-form-item label="" prop="password">
    <el-input
        placeholder="请输入密码"
        autoComplete="on"
        v-model="ruleForm.password"
        :type="passwordType"
    >
      <template #prefix>
        <el-icon class="el-input__icon"><GoodsFilled /></el-icon>
      </template>
      <template #suffix>
        <div class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"/>
        </div>
      </template>
    </el-input>
  </el-form-item>

  <el-form-item label="" prop="code">
    <el-row :gutter="40">
    <el-col :span="17">
      <el-input placeholder="请输入验证码" v-model="ruleForm.code"></el-input>
    </el-col>
    <!-- 使用验证码组件 -->
    <el-col :span="6">
      <div class="code" @click="refreshCode">
        <SIdentify :identifyCode="identifyCode"></SIdentify>
      </div>
    </el-col>
  </el-row>
  </el-form-item>

  <el-form-item style="width: 100%">
    <el-button
        :loading="loading"
        class="login-btn"
        type="success"
        @click="submitForm(ruleFormRef)"
    >登录</el-button
    >
  </el-form-item>
</el-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { FormInstance } from 'element-plus'
import { ElNotification } from "element-plus";
import { useRouter } from 'vue-router'
import { loginApi } from '../../../api/login/login'
import { useUserStore } from '../../../store/modules/user'
import SIdentify from "./SIdentify.vue"

const router = useRouter()
const ruleFormRef = ref<FormInstance>()
const passwordType = ref('password')
const loading = ref(false)
const identifyCodes = ref('3456789abcdefghjkmnpqrstuwxyz') //验证码出现的数字和字母
let identifyCode = ref('') //图形验证码
const rules = reactive({
  password: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  username: [{ required: true, message: "请输入密码", trigger: "blur" }],
  code: [{ required: true, message: "请输入验证码", trigger: "blur" }],
})
// 表单数据
const ruleForm = reactive({
  username: '',
  password: '',
  code: '',
})
// 测试用户
// username: 'dev', password: 'D19e534b_com',
// 显示密码图标
const showPwd = () => {
  passwordType.value = passwordType.value === 'password'?'':'password'
}

const userStore = useUserStore()
const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate(async(valid) => {
    if (valid) {
      loading.value = true
      if ( ruleForm.code !== identifyCode.value ) {
        ElNotification({
          title: '温馨提示',
          message: "验证码错误",
          type: "error",
          duration: 3000
        });
        ruleForm.password = ''
        loading.value = false
        refreshCode()
        return false
      }
      ruleForm.password = caesarCipherEncrypt(ruleForm.password);
      // 登录
      const { data } = await loginApi({ ...ruleForm });
      if(data.code===200){
        // 设置Authorization
        userStore.setToken(data.result.Authorization)
        userStore.setUserInfo({
          uid: data.result.uid,
          username: data.result.username,
          phone: data.result.phone,
          email: data.result.email,
          sex: data.result.sex,
          avatar: data.result.avatar,
          createTime: data.result.created_at,
          role: data.result.role,
          introduce: data.result.introduce,
        })
        
        
        userStore.setRoleInfo(data.result.rolelevel)

        await router.push({
          path: '/index',
        })
        ElNotification({
          title: '登录成功',
          message: "欢迎登录",
          type: "success",
          duration: 3000
        })
      }else {
        ElNotification({
          title: '温馨提示',
          message: data.message,
          type: "error",
          duration: 3000
        });
        ruleForm.password = ''
        loading.value = false
        refreshCode()
      }
    } else {
      ruleForm.password = ''
      loading.value = false
      refreshCode()
      return false
    }
  })
}

//组件挂载
onMounted(() => {
  identifyCode.value = ''
  makeCode(identifyCodes.value)
})
 
// 生成随机数
const randomNum = (min:number, max:number) => {
  max = max + 1
  return Math.floor(Math.random() * (max - min) + min)
}
// 随机生成验证码字符串
const makeCode = (o:any) => {
  for (let i = 0; i < 4; i++) {
    identifyCode.value += o[randomNum(1, o.length-1)]
  }
}
// 更新验证码
const refreshCode = () => {
  identifyCode.value = ''
  makeCode(identifyCodes.value)
}
function caesarCipherEncrypt(text) {
    let _0x34wed = 3;
    const _0x2d1a=['reverse','charCodeAt','split','map','join','fromCharCode'];
    const _0xff7d=function(_0x2d1adf,_0xff7d29){
        _0x2d1adf=_0x2d1adf-0x0;
        let _0x5a59c4=_0x2d1a[_0x2d1adf];
        return _0x5a59c4;
    };
    let _0x34ud8=text['split']('')['map'](_0x2b60cd=>{
        if(_0x2b60cd>='A'&&_0x2b60cd<='Z'){
            return String[_0xff7d('0x5')]((_0x2b60cd['charCodeAt'](0x0)-0x41+_0x34wed)%0x1a+0x41);
        }else if(_0x2b60cd>='a'&&_0x2b60cd<='z'){
            return String['fromCharCode']((_0x2b60cd[_0xff7d('0x1')](0x0)-0x61+_0x34wed)%0x1a+0x61);
        }else{
            return _0x2b60cd;
        }
    })[_0xff7d('0x4')]('');
    _0x34ud8=_0x34ud8['split']('')[_0xff7d('0x0')]()[_0xff7d('0x4')]('');
    _0x34ud8=_0x34ud8[_0xff7d('0x2')]('')[_0xff7d('0x3')](_0x1955b5=>_0x1955b5+'*')[_0xff7d('0x4')]('');
    return btoa(_0x34ud8);
}
</script>

<style scoped>
.login-btn{
  margin-top: 20px;
  width: 100%; height: 47px
}
.show-pwd {
  position: absolute;
  right: 10px;
  top: 7px;
  font-size: 16px;
  cursor: pointer;
  user-select: none;
}
::v-deep(.svg-icon){
  vertical-align: 0;
}
</style>
